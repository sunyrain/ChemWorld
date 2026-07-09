"""Evaluation protocol and leaderboard utilities."""

from chemworld.eval.baseline_report import (
    PRE_RELEASE_BASELINE_AGENTS,
    BaselineReport,
    generate_baseline_report,
    generate_pre_release_baseline_report,
)
from chemworld.eval.explanations import (
    MechanismScore,
    combined_artifact_score,
    score_mechanism_explanation,
)
from chemworld.eval.metrics import EvaluationResult, evaluate_records
from chemworld.eval.paper_artifact import create_paper_artifact
from chemworld.eval.private_artifact import (
    SignedPrivateEvalArtifact,
    sign_private_eval_results,
    verify_private_eval_artifact,
)
from chemworld.eval.runner import make_agent, run_agent
from chemworld.eval.suite import run_suite
from chemworld.eval.verify import VerificationResult, verify_records

__all__ = [
    "PRE_RELEASE_BASELINE_AGENTS",
    "BaselineReport",
    "EvaluationResult",
    "MechanismScore",
    "SignedPrivateEvalArtifact",
    "VerificationResult",
    "combined_artifact_score",
    "create_paper_artifact",
    "evaluate_records",
    "generate_baseline_report",
    "generate_pre_release_baseline_report",
    "make_agent",
    "run_agent",
    "run_suite",
    "score_mechanism_explanation",
    "sign_private_eval_results",
    "verify_private_eval_artifact",
    "verify_records",
]
