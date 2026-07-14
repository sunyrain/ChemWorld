"""Independent, task-agnostic reference portfolio builder v0.4.

The builder consumes only normalized public design dimensions and completed
experiment summaries supplied by the reference harness.  It deliberately does
not import evaluated agents, checkpoints, prompts, or hidden world state.
"""

from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass
from typing import Literal

SourceProfile = Literal[
    "global_space_filling",
    "ensemble_surrogate",
    "evolutionary_search",
    "risk_aware_global",
]

SOURCE_PROFILES: tuple[SourceProfile, ...] = (
    "global_space_filling",
    "ensemble_surrogate",
    "evolutionary_search",
    "risk_aware_global",
)


@dataclass(frozen=True, slots=True)
class ReferenceObservation:
    """One public completed-experiment result in normalized design space."""

    candidate: tuple[float, ...]
    objective: float
    constraint_valid: bool


def propose_normalized_candidates(
    profile: SourceProfile,
    *,
    namespace: str,
    task_id: str,
    pair_index: int,
    dimension_count: int,
    count: int,
    observations: tuple[ReferenceObservation, ...] = (),
) -> tuple[tuple[float, ...], ...]:
    """Return deterministic candidates in ``[0, 1]^d`` for one source stream."""

    if profile not in SOURCE_PROFILES:
        raise ValueError(f"unsupported reference source profile: {profile}")
    if not namespace or not task_id or pair_index < 0 or dimension_count < 1 or count < 1:
        raise ValueError("invalid reference builder identity or dimensions")
    _validate_observations(observations, dimension_count)
    seed = _derived_seed(namespace, task_id, pair_index, profile)
    if profile == "global_space_filling":
        return _halton_candidates(seed, dimension_count, count)
    rng = random.Random(seed)
    pool = tuple(
        tuple(rng.random() for _ in range(dimension_count))
        for _ in range(max(256, count * 32))
    )
    if not observations:
        return pool[:count]
    if profile == "evolutionary_search":
        return _evolutionary_candidates(rng, observations, dimension_count, count)
    risk_aware = profile == "risk_aware_global"
    ranked = sorted(
        pool,
        key=lambda candidate: _acquisition(candidate, observations, risk_aware=risk_aware),
        reverse=True,
    )
    return tuple(ranked[:count])


def _acquisition(
    candidate: tuple[float, ...],
    observations: tuple[ReferenceObservation, ...],
    *,
    risk_aware: bool,
) -> float:
    neighbours = sorted(observations, key=lambda row: _distance(candidate, row.candidate))[:8]
    weights = [1.0 / max(_distance(candidate, row.candidate), 1e-9) for row in neighbours]
    total = sum(weights)
    mean = sum(
        weight * row.objective for weight, row in zip(weights, neighbours, strict=True)
    ) / total
    spread = math.sqrt(
        sum(
            weight * (row.objective - mean) ** 2
            for weight, row in zip(weights, neighbours, strict=True)
        )
        / total
    )
    novelty = min(_distance(candidate, row.candidate) for row in observations)
    feasibility = sum(
        weight * float(row.constraint_valid)
        for weight, row in zip(weights, neighbours, strict=True)
    ) / total
    return mean + 0.35 * spread + 0.15 * novelty + (0.5 * feasibility if risk_aware else 0.0)


def _evolutionary_candidates(
    rng: random.Random,
    observations: tuple[ReferenceObservation, ...],
    dimension_count: int,
    count: int,
) -> tuple[tuple[float, ...], ...]:
    parents = sorted(
        observations,
        key=lambda row: (row.constraint_valid, row.objective),
        reverse=True,
    )[: max(2, min(8, len(observations)))]
    rows: list[tuple[float, ...]] = []
    for index in range(count):
        left = parents[index % len(parents)].candidate
        right = parents[(index * 3 + 1) % len(parents)].candidate
        rows.append(
            tuple(
                min(1.0, max(0.0, (a + b) / 2.0 + rng.gauss(0.0, 0.08)))
                for a, b in zip(left, right, strict=True)
            )
        )
    return tuple(rows)


def _halton_candidates(
    seed: int, dimension_count: int, count: int
) -> tuple[tuple[float, ...], ...]:
    primes = _first_primes(dimension_count)
    offset = 1 + seed % 10_000
    return tuple(
        tuple(_radical_inverse(offset + index, base) for base in primes)
        for index in range(count)
    )


def _derived_seed(namespace: str, task_id: str, pair_index: int, profile: str) -> int:
    digest = hashlib.sha256(
        f"{namespace}\0{task_id}\0{pair_index}\0{profile}".encode()
    ).digest()
    return int.from_bytes(digest[:8], "big")


def _validate_observations(
    observations: tuple[ReferenceObservation, ...], dimension_count: int
) -> None:
    for row in observations:
        if len(row.candidate) != dimension_count or not math.isfinite(row.objective):
            raise ValueError("reference observation shape or objective is invalid")
        if any(not math.isfinite(value) or not 0.0 <= value <= 1.0 for value in row.candidate):
            raise ValueError("reference observation candidate must be finite and normalized")


def _distance(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right, strict=True)))


def _radical_inverse(index: int, base: int) -> float:
    value = 0.0
    factor = 1.0 / base
    while index:
        index, digit = divmod(index, base)
        value += digit * factor
        factor /= base
    return value


def _first_primes(count: int) -> tuple[int, ...]:
    primes: list[int] = []
    candidate = 2
    while len(primes) < count:
        if all(candidate % prime for prime in primes if prime * prime <= candidate):
            primes.append(candidate)
        candidate += 1
    return tuple(primes)


__all__ = ["SOURCE_PROFILES", "ReferenceObservation", "propose_normalized_candidates"]
