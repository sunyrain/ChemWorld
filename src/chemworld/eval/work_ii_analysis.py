"""Frozen Work II prediction-error and cluster-contrast calculations."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


class WorkIIAnalysisError(ValueError):
    """Raised when a formal Work II analysis record violates the frozen contract."""


@dataclass(frozen=True)
class PredictionErrorSummary:
    error: float
    term_count: int
    terms: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "error": self.error,
            "term_count": self.term_count,
            "terms": [dict(item) for item in self.terms],
        }


@dataclass(frozen=True)
class ClusterCorrectionContrast:
    misindexed_improvement: float
    aligned_improvement: float
    primary_contrast: float

    def to_dict(self) -> dict[str, float]:
        return {
            "misindexed_improvement": self.misindexed_improvement,
            "aligned_improvement": self.aligned_improvement,
            "primary_contrast": self.primary_contrast,
        }


def _finite_number(value: Any, *, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise WorkIIAnalysisError(f"{field} must be numeric")
    number = float(value)
    if not math.isfinite(number):
        raise WorkIIAnalysisError(f"{field} must be finite")
    return number


def score_prediction_error(
    predictions: Sequence[Mapping[str, Any]],
    evaluator_truth: Mapping[str, Mapping[str, Any]],
    *,
    metric_scales: Mapping[str, float] | None = None,
    default_metric_scale: float = 1.0,
) -> PredictionErrorSummary:
    """Return the un-clipped mean normalized absolute error over exact query/metric pairs."""

    if not math.isfinite(default_metric_scale) or default_metric_scale <= 0.0:
        raise WorkIIAnalysisError("default_metric_scale must be finite and positive")
    prediction_by_query: dict[str, Mapping[str, Any]] = {}
    for item in predictions:
        query_id = str(item.get("query_id", ""))
        if not query_id or query_id in prediction_by_query:
            raise WorkIIAnalysisError("prediction query IDs must be non-empty and unique")
        prediction_by_query[query_id] = item
    if set(prediction_by_query) != set(evaluator_truth):
        raise WorkIIAnalysisError("prediction queries must exactly match evaluator truth queries")

    scales = dict(metric_scales or {})
    terms: list[dict[str, Any]] = []
    for query_id in evaluator_truth:
        truth_metrics = evaluator_truth[query_id]
        metrics = prediction_by_query[query_id].get("metrics")
        if not isinstance(metrics, Sequence) or isinstance(metrics, str | bytes):
            raise WorkIIAnalysisError(f"predictions[{query_id}].metrics must be a list")
        prediction_metrics: dict[str, Mapping[str, Any]] = {}
        for metric in metrics:
            if not isinstance(metric, Mapping):
                raise WorkIIAnalysisError("prediction metric rows must be objects")
            metric_id = str(metric.get("metric_id", ""))
            if not metric_id or metric_id in prediction_metrics:
                raise WorkIIAnalysisError("prediction metric IDs must be non-empty and unique")
            prediction_metrics[metric_id] = metric
        if set(prediction_metrics) != set(truth_metrics):
            raise WorkIIAnalysisError(
                f"prediction metrics for {query_id} must exactly match evaluator truth"
            )
        for metric_id in truth_metrics:
            predicted = _finite_number(
                prediction_metrics[metric_id].get("mean"),
                field=f"{query_id}.{metric_id}.mean",
            )
            truth = _finite_number(
                truth_metrics[metric_id],
                field=f"{query_id}.{metric_id}.truth",
            )
            scale = _finite_number(
                scales.get(metric_id, default_metric_scale),
                field=f"metric_scales.{metric_id}",
            )
            if scale <= 0.0:
                raise WorkIIAnalysisError(f"metric scale for {metric_id} must be positive")
            terms.append(
                {
                    "query_id": query_id,
                    "metric_id": metric_id,
                    "predicted_mean": predicted,
                    "evaluator_truth": truth,
                    "metric_scale": scale,
                    "normalized_absolute_error": abs(predicted - truth) / scale,
                }
            )
    if not terms:
        raise WorkIIAnalysisError("prediction error requires at least one query/metric term")
    return PredictionErrorSummary(
        error=sum(item["normalized_absolute_error"] for item in terms) / len(terms),
        term_count=len(terms),
        terms=tuple(terms),
    )


def correction_contrast(
    *,
    misindexed_pre: float,
    misindexed_final: float | None,
    aligned_pre: float,
    aligned_final: float | None,
) -> ClusterCorrectionContrast:
    """Apply frozen zero-improvement missing-final handling and calculate H3."""

    mis_pre = _finite_number(misindexed_pre, field="misindexed_pre")
    aligned_pre_value = _finite_number(aligned_pre, field="aligned_pre")
    mis_final = (
        mis_pre
        if misindexed_final is None
        else _finite_number(misindexed_final, field="misindexed_final")
    )
    aligned_final_value = (
        aligned_pre_value
        if aligned_final is None
        else _finite_number(aligned_final, field="aligned_final")
    )
    mis_improvement = mis_pre - mis_final
    aligned_improvement = aligned_pre_value - aligned_final_value
    return ClusterCorrectionContrast(
        misindexed_improvement=mis_improvement,
        aligned_improvement=aligned_improvement,
        primary_contrast=mis_improvement - aligned_improvement,
    )


__all__ = [
    "ClusterCorrectionContrast",
    "PredictionErrorSummary",
    "WorkIIAnalysisError",
    "correction_contrast",
    "score_prediction_error",
]
