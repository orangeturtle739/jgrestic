import os
import secrets
import subprocess
from pathlib import Path

import click
import toml

from jgrestic.commands import restic
from jgrestic.restic_files import ResticFiles


@click.command()
@click.argument("src", type=click.Path(file_okay=False, dir_okay=True, exists=True))
@click.argument(
    "root", type=click.Path(file_okay=False, dir_okay=True, exists=True, writable=True)
)
@click.pass_context
def init(ctx: click.Context, src: str, root: str) -> None:
    """
    Creates a new jgrestic repository.

    The repository will backup SRC to ROOT. ROOT and SRC
    must both be directories.
    """

    files = ResticFiles.from_root(Path(root))
    if any(True for _ in files.root.iterdir()):
        ctx.fail(f"Repository is not empty: {files.root}")

    with files.password.open("wb") as out:
        out.write(secrets.token_bytes(512))

    with files.config.open("w") as config_out:
        toml.dump({"src": str(Path(src).resolve())}, config_out)

    subprocess.run([restic, "init"], check=True, env={**os.environ, **files.env()})
    click.secho(f"Created new repository at {root}", fg="green")
