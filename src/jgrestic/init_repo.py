import argparse
import os
import secrets
import subprocess
import typing as t
from pathlib import Path

import toml

from jgrestic.commands import restic
from jgrestic.restic_files import ResticFiles
from jgrestic.subcommand import Subcommand


class InitRepo(Subcommand):
    def name(self) -> str:
        return "init-repo"

    def help(self) -> str:
        return "Initialize a new restic repository"

    def configure(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--root", help="Backup location", required=True,
        )
        parser.add_argument(
            "--backup-src", help="Folder which will be backed up", required=True,
        )

    def run(self, args: t.Any) -> int:
        root = Path(args.root)
        if not root.is_dir():
            print(f"{root} is not a directory")
            return 1
        backup_src = Path(args.backup_src)
        if not backup_src.is_dir():
            print(f"{backup_src} is not a directory")
            return 1

        files = ResticFiles.from_root(root)

        with files.password.open("wb") as out:
            out.write(secrets.token_bytes(512))

        with files.config.open("w") as config_out:
            toml.dump({"backup_src": str(backup_src.resolve())}, config_out)

        files.repo.mkdir()
        subprocess.run([restic, "init"], check=True, env={**os.environ, **files.env()})

        return 0
