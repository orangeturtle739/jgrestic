import argparse
import sys

from jgrestic.backup import Backup
from jgrestic.init_repo import InitRepo
from jgrestic.subcommand import invoke_subcommand, register_subcommands


def main() -> int:
    parser = argparse.ArgumentParser(description="Restic backup tool")
    register_subcommands(
        parser, title="cmd", subcommands=[InitRepo(), Backup()],
    )
    args = parser.parse_args()
    return invoke_subcommand("cmd", args)


def wrapper() -> None:
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
