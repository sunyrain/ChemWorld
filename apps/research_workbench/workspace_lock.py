"""An OS lock prevents concurrent writers to a local workspace."""

from __future__ import annotations

import os
from pathlib import Path


class WorkspaceLock:
    def __init__(self, root: Path) -> None:
        root.mkdir(parents=True, exist_ok=True)
        self.handle = (root / ".workbench.lock").open("a+b")
        if self.handle.seek(0, 2) == 0:
            self.handle.write(b"0")
            self.handle.flush()
        self.handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.handle.close()
            raise ValueError("Workspace is already open in another workbench process") from None

    def close(self) -> None:
        self.handle.close()  # Closing the descriptor releases the OS lock on both platforms.
