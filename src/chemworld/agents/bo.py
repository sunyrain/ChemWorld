"""Surrogate-model optimization baselines."""

from __future__ import annotations

import warnings
from math import erf, pi, sqrt
from typing import Any

import numpy as np
from sklearn.exceptions import ConvergenceWarning

from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.recipe_sequence import RecipeSequenceMixin
from chemworld.agents.task_recipes import (
    sample_task_recipe,
    task_recipe_event_count,
    task_recipe_to_vector,
)


def _normal_cdf(z: np.ndarray) -> np.ndarray:
    return 0.5 * (1.0 + np.vectorize(erf)(z / sqrt(2.0)))


def _normal_pdf(z: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * z**2) / sqrt(2.0 * pi)


def _expected_improvement(
    mu: np.ndarray,
    sigma: np.ndarray,
    best: float,
    xi: float = 0.01,
) -> np.ndarray:
    sigma = np.maximum(sigma, 1.0e-9)
    improvement = mu - best - xi
    z = improvement / sigma
    return improvement * _normal_cdf(z) + sigma * _normal_pdf(z)


def _probability_improvement(
    mu: np.ndarray,
    sigma: np.ndarray,
    best: float,
    xi: float = 0.01,
) -> np.ndarray:
    sigma = np.maximum(sigma, 1.0e-9)
    return _normal_cdf((mu - best - xi) / sigma)


class CandidateSurrogateMixin:
    rng: np.random.Generator
    task_info: dict[str, Any]

    def _start_recipe(self, action: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def _reset_surrogate_diagnostics(self) -> None:
        self._decision_trace: list[dict[str, Any]] = []

    def _start_surrogate_recipe(
        self,
        action: dict[str, Any],
        *,
        phase: str,
        trained_recipe_count: int,
        best_observed_score: float | None = None,
        acquisition_value: float | None = None,
        selected_policy: str,
    ) -> dict[str, Any]:
        self._decision_trace.append(
            {
                "trace_type": "surrogate_recipe_decision",
                "phase": phase,
                "trained_recipe_count": trained_recipe_count,
                "used_surrogate": phase == "acquisition",
                "selected_policy": selected_policy,
                "best_observed_score": best_observed_score,
                "acquisition_value": acquisition_value,
                "selected_recipe": dict(action),
            }
        )
        return self._start_recipe(action)

    def agent_trace(self) -> list[dict[str, Any]]:
        return [dict(item) for item in getattr(self, "_decision_trace", [])]

    def _candidate_actions(self, count: int) -> list[dict[str, Any]]:
        return [sample_task_recipe(self.task_info, self.rng) for _ in range(count)]

    def _xy(self, history: list[HistoryRecord]) -> tuple[np.ndarray, np.ndarray]:
        x = np.vstack([task_recipe_to_vector(record.action) for record in history])
        y = np.asarray([record.reward for record in history], dtype=float)
        return x, y


class GaussianProcessBOAgent(RecipeSequenceMixin, CandidateSurrogateMixin, BaseAgent):
    name = "gp_bo"

    def __init__(self, n_initial: int = 4, n_candidates: int = 512) -> None:
        self.n_initial = n_initial
        self.n_candidates = n_candidates
        self.effective_n_initial = n_initial

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self.rng = np.random.default_rng(seed)
        experiment_capacity = max(
            1,
            int(task_info.get("budget", 1)) // task_recipe_event_count(task_info),
        )
        self.effective_n_initial = min(
            self.n_initial,
            max(1, experiment_capacity - 1),
        )
        self._reset_surrogate_diagnostics()

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending

        recipe_history = self._recipe_history
        if len(recipe_history) < self.effective_n_initial:
            return self._start_surrogate_recipe(
                sample_task_recipe(self.task_info, self.rng),
                phase="initial",
                trained_recipe_count=len(recipe_history),
                selected_policy="random_initial_design",
            )

        candidates, y_train, mu, sigma = self._candidate_predictions(recipe_history)
        acquisition = _expected_improvement(mu, sigma, best=float(np.max(y_train)))
        selected_index = int(np.argmax(acquisition))
        return self._start_surrogate_recipe(
            candidates[selected_index],
            phase="acquisition",
            trained_recipe_count=len(recipe_history),
            best_observed_score=float(np.max(y_train)),
            acquisition_value=float(acquisition[selected_index]),
            selected_policy="gp_expected_improvement",
        )

    def _candidate_predictions(
        self,
        recipe_history: list[HistoryRecord],
    ) -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray, np.ndarray]:
        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import Matern, WhiteKernel

        x_train, y_train = self._xy(recipe_history)
        kernel = Matern(length_scale=np.ones(x_train.shape[1]), nu=2.5) + WhiteKernel(
            noise_level=1.0e-4
        )
        model = GaussianProcessRegressor(kernel=kernel, normalize_y=True, random_state=self.seed)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ConvergenceWarning)
            model.fit(x_train, y_train)
        candidates = self._candidate_actions(self.n_candidates)
        x_candidates = np.vstack([task_recipe_to_vector(action) for action in candidates])
        mu, sigma = model.predict(x_candidates, return_std=True)
        return candidates, y_train, mu, sigma

    def manifest(self) -> dict[str, Any]:
        manifest = super().manifest()
        manifest.update(
            {
                "surrogate_family": "gaussian_process",
                "n_initial": self.n_initial,
                "effective_n_initial": self.effective_n_initial,
                "n_candidates": self.n_candidates,
            }
        )
        return manifest


class GaussianProcessPIAgent(GaussianProcessBOAgent):
    """Gaussian-process optimization using probability of improvement."""

    name = "gp_pi"

    def __init__(self, n_initial: int = 4, n_candidates: int = 512, xi: float = 0.01) -> None:
        super().__init__(n_initial=n_initial, n_candidates=n_candidates)
        self.xi = xi

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending
        recipe_history = self._recipe_history
        if len(recipe_history) < self.effective_n_initial:
            return self._start_surrogate_recipe(
                sample_task_recipe(self.task_info, self.rng),
                phase="initial",
                trained_recipe_count=len(recipe_history),
                selected_policy="random_initial_design",
            )
        candidates, y_train, mu, sigma = self._candidate_predictions(recipe_history)
        acquisition = _probability_improvement(
            mu,
            sigma,
            best=float(np.max(y_train)),
            xi=self.xi,
        )
        selected_index = int(np.argmax(acquisition))
        return self._start_surrogate_recipe(
            candidates[selected_index],
            phase="acquisition",
            trained_recipe_count=len(recipe_history),
            best_observed_score=float(np.max(y_train)),
            acquisition_value=float(acquisition[selected_index]),
            selected_policy="gp_probability_improvement",
        )

    def manifest(self) -> dict[str, Any]:
        manifest = super().manifest()
        manifest.update({"acquisition_function": "probability_improvement", "xi": self.xi})
        return manifest


class GaussianProcessUCBAgent(GaussianProcessBOAgent):
    """Gaussian-process optimization using an upper-confidence bound."""

    name = "gp_ucb"

    def __init__(
        self,
        n_initial: int = 4,
        n_candidates: int = 512,
        exploration_weight: float = 2.0,
    ) -> None:
        super().__init__(n_initial=n_initial, n_candidates=n_candidates)
        self.exploration_weight = exploration_weight

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending
        recipe_history = self._recipe_history
        if len(recipe_history) < self.effective_n_initial:
            return self._start_surrogate_recipe(
                sample_task_recipe(self.task_info, self.rng),
                phase="initial",
                trained_recipe_count=len(recipe_history),
                selected_policy="random_initial_design",
            )
        candidates, y_train, mu, sigma = self._candidate_predictions(recipe_history)
        acquisition = mu + self.exploration_weight * sigma
        selected_index = int(np.argmax(acquisition))
        return self._start_surrogate_recipe(
            candidates[selected_index],
            phase="acquisition",
            trained_recipe_count=len(recipe_history),
            best_observed_score=float(np.max(y_train)),
            acquisition_value=float(acquisition[selected_index]),
            selected_policy="gp_upper_confidence_bound",
        )

    def manifest(self) -> dict[str, Any]:
        manifest = super().manifest()
        manifest.update(
            {
                "acquisition_function": "upper_confidence_bound",
                "exploration_weight": self.exploration_weight,
            }
        )
        return manifest


class RandomForestEIAgent(RecipeSequenceMixin, CandidateSurrogateMixin, BaseAgent):
    name = "rf_ei"

    def __init__(
        self,
        n_initial: int = 4,
        n_candidates: int = 512,
        n_estimators: int = 128,
    ) -> None:
        self.n_initial = n_initial
        self.n_candidates = n_candidates
        self.n_estimators = n_estimators
        self.effective_n_initial = n_initial

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self.rng = np.random.default_rng(seed)
        experiment_capacity = max(
            1,
            int(task_info.get("budget", 1)) // task_recipe_event_count(task_info),
        )
        self.effective_n_initial = min(
            self.n_initial,
            max(1, experiment_capacity - 1),
        )
        self._reset_surrogate_diagnostics()

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending

        recipe_history = self._recipe_history
        if len(recipe_history) < self.effective_n_initial:
            return self._start_surrogate_recipe(
                sample_task_recipe(self.task_info, self.rng),
                phase="initial",
                trained_recipe_count=len(recipe_history),
                selected_policy="random_initial_design",
            )

        from sklearn.ensemble import RandomForestRegressor

        x_train, y_train = self._xy(recipe_history)
        model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            min_samples_leaf=2,
            random_state=self.seed,
        )
        model.fit(x_train, y_train)

        candidates = self._candidate_actions(self.n_candidates)
        x_candidates = np.vstack([task_recipe_to_vector(action) for action in candidates])
        tree_predictions = np.vstack([tree.predict(x_candidates) for tree in model.estimators_])
        mu = tree_predictions.mean(axis=0)
        sigma = tree_predictions.std(axis=0)
        acquisition = _expected_improvement(mu, sigma, best=float(np.max(y_train)))
        selected_index = int(np.argmax(acquisition))
        return self._start_surrogate_recipe(
            candidates[selected_index],
            phase="acquisition",
            trained_recipe_count=len(recipe_history),
            best_observed_score=float(np.max(y_train)),
            acquisition_value=float(acquisition[selected_index]),
            selected_policy="rf_expected_improvement",
        )

    def manifest(self) -> dict[str, Any]:
        manifest = super().manifest()
        manifest.update(
            {
                "surrogate_family": "random_forest",
                "n_initial": self.n_initial,
                "effective_n_initial": self.effective_n_initial,
                "n_candidates": self.n_candidates,
                "n_estimators": self.n_estimators,
            }
        )
        return manifest


class SafetyConstrainedBOAgent(GaussianProcessBOAgent):
    name = "safe_gp_bo"

    def __init__(
        self,
        n_initial: int = 4,
        n_candidates: int = 768,
        risk_threshold: float = 0.65,
    ) -> None:
        super().__init__(n_initial=n_initial, n_candidates=n_candidates)
        self.risk_threshold = risk_threshold
        self.effective_risk_threshold = risk_threshold

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        task_limit = float(task_info.get("safety_limit", self.risk_threshold))
        self.effective_risk_threshold = min(self.risk_threshold, task_limit)

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending

        recipe_history = self._recipe_history
        if len(recipe_history) < self.effective_n_initial:
            return self._start_surrogate_recipe(
                sample_task_recipe(self.task_info, self.rng),
                phase="initial",
                trained_recipe_count=len(recipe_history),
                selected_policy="random_initial_design",
            )

        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import Matern, WhiteKernel

        x_train, y_train = self._xy(recipe_history)
        risk_train = np.asarray(
            [record.observation.get("safety_risk", 1.0) for record in recipe_history],
            dtype=float,
        )
        kernel = Matern(length_scale=np.ones(x_train.shape[1]), nu=2.5) + WhiteKernel(
            noise_level=1.0e-4
        )

        score_model = GaussianProcessRegressor(
            kernel=kernel,
            normalize_y=True,
            random_state=self.seed,
        )
        risk_model = GaussianProcessRegressor(
            kernel=kernel,
            normalize_y=True,
            random_state=self.seed + 1,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ConvergenceWarning)
            score_model.fit(x_train, y_train)
            risk_model.fit(x_train, risk_train)

        candidates = self._candidate_actions(self.n_candidates)
        x_candidates = np.vstack([task_recipe_to_vector(action) for action in candidates])
        mu, sigma = score_model.predict(x_candidates, return_std=True)
        risk_mu, risk_sigma = risk_model.predict(x_candidates, return_std=True)
        acquisition = _expected_improvement(mu, sigma, best=float(np.max(y_train)))

        safety_margin = risk_mu + 0.5 * risk_sigma
        safe_mask = safety_margin <= self.effective_risk_threshold
        if np.any(safe_mask):
            acquisition = np.where(safe_mask, acquisition, -np.inf)
            selected_index = int(np.argmax(acquisition))
            return self._start_surrogate_recipe(
                candidates[selected_index],
                phase="acquisition",
                trained_recipe_count=len(recipe_history),
                best_observed_score=float(np.max(y_train)),
                acquisition_value=float(acquisition[selected_index]),
                selected_policy="safe_gp_expected_improvement",
            )

        selected_index = int(np.argmin(safety_margin))
        return self._start_surrogate_recipe(
            candidates[selected_index],
            phase="acquisition",
            trained_recipe_count=len(recipe_history),
            best_observed_score=float(np.max(y_train)),
            acquisition_value=float(acquisition[selected_index]),
            selected_policy="safe_gp_risk_fallback",
        )

    def manifest(self) -> dict[str, Any]:
        manifest = super().manifest()
        manifest.update(
            {
                "surrogate_family": "safe_gaussian_process",
                "configured_risk_threshold": self.risk_threshold,
                "risk_threshold": self.effective_risk_threshold,
            }
        )
        return manifest
