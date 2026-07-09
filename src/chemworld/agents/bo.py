"""Surrogate-model optimization baselines."""

from __future__ import annotations

import warnings
from math import erf, pi, sqrt
from typing import Any

import numpy as np
from sklearn.exceptions import ConvergenceWarning

from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.recipe_sequence import RecipeSequenceMixin
from chemworld.world.actions import action_to_vector, sample_random_action


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


class CandidateSurrogateMixin:
    rng: np.random.Generator

    def _candidate_actions(self, count: int) -> list[dict[str, Any]]:
        return [sample_random_action(self.rng) for _ in range(count)]

    @staticmethod
    def _xy(history: list[HistoryRecord]) -> tuple[np.ndarray, np.ndarray]:
        x = np.vstack([action_to_vector(record.action) for record in history])
        y = np.asarray([record.reward for record in history], dtype=float)
        return x, y


class GaussianProcessBOAgent(RecipeSequenceMixin, CandidateSurrogateMixin, BaseAgent):
    name = "gp_bo"

    def __init__(self, n_initial: int = 4, n_candidates: int = 512) -> None:
        self.n_initial = n_initial
        self.n_candidates = n_candidates

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self.rng = np.random.default_rng(seed)

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending

        recipe_history = self._recipe_history
        if len(recipe_history) < self.n_initial:
            return self._start_recipe(sample_random_action(self.rng))

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
        x_candidates = np.vstack([action_to_vector(action) for action in candidates])
        mu, sigma = model.predict(x_candidates, return_std=True)
        acquisition = _expected_improvement(mu, sigma, best=float(np.max(y_train)))
        return self._start_recipe(candidates[int(np.argmax(acquisition))])


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

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self.rng = np.random.default_rng(seed)

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending

        recipe_history = self._recipe_history
        if len(recipe_history) < self.n_initial:
            return self._start_recipe(sample_random_action(self.rng))

        from sklearn.ensemble import RandomForestRegressor

        x_train, y_train = self._xy(recipe_history)
        model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            min_samples_leaf=2,
            random_state=self.seed,
        )
        model.fit(x_train, y_train)

        candidates = self._candidate_actions(self.n_candidates)
        x_candidates = np.vstack([action_to_vector(action) for action in candidates])
        tree_predictions = np.vstack([tree.predict(x_candidates) for tree in model.estimators_])
        mu = tree_predictions.mean(axis=0)
        sigma = tree_predictions.std(axis=0)
        acquisition = _expected_improvement(mu, sigma, best=float(np.max(y_train)))
        return self._start_recipe(candidates[int(np.argmax(acquisition))])


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

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending

        recipe_history = self._recipe_history
        if len(recipe_history) < self.n_initial:
            return self._start_recipe(sample_random_action(self.rng))

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
        x_candidates = np.vstack([action_to_vector(action) for action in candidates])
        mu, sigma = score_model.predict(x_candidates, return_std=True)
        risk_mu, risk_sigma = risk_model.predict(x_candidates, return_std=True)
        acquisition = _expected_improvement(mu, sigma, best=float(np.max(y_train)))

        safety_margin = risk_mu + 0.5 * risk_sigma
        safe_mask = safety_margin <= self.risk_threshold
        if np.any(safe_mask):
            acquisition = np.where(safe_mask, acquisition, -np.inf)
            return self._start_recipe(candidates[int(np.argmax(acquisition))])

        return self._start_recipe(candidates[int(np.argmin(safety_margin))])
