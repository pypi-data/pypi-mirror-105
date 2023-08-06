import argparse
import subprocess
import sys

from typing import List

from precompose_utils.clean import clean
from precompose_utils.paths import APPS
from precompose_utils.lockfile import locklib


@locklib
def unmount(app: str, verbose: bool = False, force: bool = False):
    appdir = APPS.joinpath(app)
    if not appdir.exists():
        raise RuntimeError(f"{app}: not mounted")

    if not appdir.is_symlink():
        raise RuntimeError(f"{app}: not a symlink")

    if not force:
        running = (
            subprocess.run(
                ["docker-compose", "ps", "-q"],
                cwd=appdir,
                stdout=subprocess.PIPE,
                check=True,
            )
            .stdout.decode()
            .strip()
        )

        if len(running) > 0:
            raise RuntimeError(f"{app} still has containers!")

    checkout = appdir.resolve().parent
    appdir.unlink()
    clean([checkout], verbose=verbose)


def main(argv: List[str] = sys.argv[1:]) -> int:
    parser = argparse.ArgumentParser(
        prog="precompose-unmount",
        description="Unmount a precomposed application",
    )

    parser.add_argument("app", metavar="APP", help="app to unmount")
    parser.add_argument("--quiet", action="store_true", help="suppress output")
    parser.add_argument(
        "--force", action="store_true", help="ignore running containers"
    )
    args = parser.parse_args(argv)

    try:
        unmount(args.app, force=args.force, verbose=not args.quiet)
        return 0
    except RuntimeError as e:
        sys.stderr.write(f"ERROR: {e}\n")
        return 1


if __name__ == "__main__":
    main()
