import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser("generate command bindings")
    parser.add_argument("outpkg", help="path to output python package")
    parser.add_argument("bindings", nargs="*", help="name=path bindings")

    args = parser.parse_args()

    outpkg = Path(args.outpkg)
    outpkg.mkdir(parents=True, exist_ok=True)
    with (outpkg / "__init__.py").open("w") as out:
        for binding in args.bindings:
            name, value = binding.split("=")
            print(f'{name} = "{value}"', file=out)
    (outpkg / "py.typed").touch()


if __name__ == "__main__":
    main()
