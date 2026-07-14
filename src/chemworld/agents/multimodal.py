"""Provider-neutral public image artifacts for multimodal agents.

Images travel to provider adapters by path plus content hashes.  Raw bytes, data URLs,
and provider-specific image objects never enter the benchmark trajectory or audit log.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import PurePosixPath
from typing import Any, Literal, Protocol

ImageSource = Literal["current", "historical"]
SpectrumDisclosure = Literal["assigned", "unassigned"]


@dataclass(frozen=True)
class PublicImageArtifact:
    """Immutable, replayable reference to one public spectrum image."""

    artifact_id: str
    spectrum_id: str
    source: ImageSource
    spectrum_kind: str
    disclosure: SpectrumDisclosure
    media_type: Literal["image/png"]
    width_px: int
    height_px: int
    x_axis_direction: Literal["ascending_left_to_right", "descending_left_to_right"]
    sha256: str
    signal_sha256: str
    public_packet_sha256: str
    render_contract_hash: str
    relative_path: str

    def __post_init__(self) -> None:
        path = PurePosixPath(self.relative_path)
        if path.is_absolute() or ".." in path.parts or path.suffix.lower() != ".png":
            raise ValueError("relative_path must be a traversal-free relative PNG path")
        if not self.artifact_id or not self.spectrum_id or not self.spectrum_kind:
            raise ValueError("artifact and spectrum identifiers must be non-empty")
        if self.width_px <= 0 or self.height_px <= 0:
            raise ValueError("image dimensions must be positive")
        for name in (
            "sha256",
            "signal_sha256",
            "public_packet_sha256",
            "render_contract_hash",
        ):
            value = getattr(self, name)
            if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")

    def to_dict(self) -> dict[str, Any]:
        """Return log-safe metadata without embedding image bytes."""

        return asdict(self)


class MultimodalJsonCompletionLike(Protocol):
    payload: dict[str, Any]
    model: str
    usage: dict[str, Any]
    attempts: int


class MultimodalJsonPlannerClientLike(Protocol):
    """Minimal provider seam for a future image-capable live-agent adapter."""

    model: str

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        images: Sequence[PublicImageArtifact],
        max_tokens: int = 4096,
    ) -> MultimodalJsonCompletionLike: ...


__all__ = [
    "ImageSource",
    "MultimodalJsonCompletionLike",
    "MultimodalJsonPlannerClientLike",
    "PublicImageArtifact",
    "SpectrumDisclosure",
]
