from __future__ import annotations

import dataclasses
import typing as t
from pathlib import Path


@dataclasses.dataclass
class ResticFiles:
    root: Path
    password: Path
    repo: Path
    config: Path

    def env(self) -> t.Dict[str, str]:
        return {
            "RESTIC_PASSWORD_FILE": str(self.password),
            "RESTIC_REPOSITORY": str(self.repo),
        }

    @staticmethod
    def from_root(root: Path) -> ResticFiles:
        return ResticFiles(
            root=root,
            password=root / "password",
            repo=root / "repo",
            config=root / "jgrestic.toml",
        )
