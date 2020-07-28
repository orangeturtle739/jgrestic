import os
import subprocess
from pathlib import Path

import click
import toml

from jgrestic.commands import restic
from jgrestic.restic_files import ResticFiles


@click.command()
@click.argument(
    "root", type=click.Path(file_okay=False, dir_okay=True, exists=True, writable=True)
)
def backup(root: str) -> None:
    """
    Initiates a backup to the to the given ROOT.

    The configuration file is from ROOT/jgrestic.toml.
    """
    files = ResticFiles.from_root(Path(root))
    src = Path(toml.load(files.config.open("r"))["src"])

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
    subprocess.run([restic, "backup", src], check=True, env=env)
