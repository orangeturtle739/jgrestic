import typing as t
from jgrestic.subcommand import Subcommand
import argparse
import toml
import subprocess
import os
from pathlib import Path
from jgrestic.restic_files import ResticFiles
from jgrestic.commands import restic


class Backup(Subcommand):
    def name(self) -> str:
        return "backup"

    def help(self) -> str:
        return "Do a backup"

    def configure(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--root", help="Backup location", required=True,
        )

    def run(self, args: t.Any) -> int:
        files = ResticFiles.from_root(Path(args.root))
        backup_src = Path(toml.load(files.config.open("r"))["backup_src"])

        env = {**os.environ, **files.env()}
        subprocess.run(
            [
                restic,
                "forget",
                "--keep-daily",
                "7",
                "--keep-weekly",
                "4",
                "--keep-monthly",
                "12",
                "--keep-yearly",
                "10",
            ],
            check=True,
            env=env,
        )
        subprocess.run([restic, "prune"], check=True, env=env)
        subprocess.run([restic, "backup", backup_src], env=env)

        return 0
