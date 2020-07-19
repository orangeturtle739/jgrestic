import argparse
from jgrestic.subcommand import register_subcommands, invoke_subcommand
from jgrestic.init_repo import InitRepo
from jgrestic.backup import Backup
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="JG restic setup")
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
