import argparse
import shutil
import sys

from pathlib import Path
from typing import List, Optional

from precompose_utils.lockfile import locklib
from precompose_utils.paths import APPS, CHECKOUTS
from precompose_utils.storage import remove_storage, remove_missing_storage


@locklib
def clean(checkouts: Optional[List[Path]] = None, verbose: bool = False):
    if checkouts is None:
        checkouts = [x for x in CHECKOUTS.iterdir() if x.is_dir()]

    for checkout in checkouts:
        in_use = False
        for app in APPS.iterdir():
            if app.is_symlink() and str(app.resolve()).startswith(
                str(checkout.resolve()) + "/"
            ):
                in_use = True
                if verbose:
                    sys.stderr.write(f"Not removing {checkout}: in use by {app}\n")
                break

        if not in_use:
            storage = checkout.joinpath("storage")
            remove_storage(storage, verbose=verbose)
            if verbose:
                sys.stderr.write(f"Removing {checkout} ...\n")
            shutil.rmtree(checkout)


def main(argv: List[str] = sys.argv[1:]) -> int:
    parser = argparse.ArgumentParser(
        prog="precompose-clean",
        description="Clean up unused checkouts",
    )
    parser.add_argument(
        "--missing", action="store_true", help="remove missing paths from storage.conf"
    )
    parser.add_argument("--quiet", action="store_true", help="suppress output")
    args = parser.parse_args(argv)

    try:
        if args.missing:
            remove_missing_storage(verbose=not args.quiet)
        else:
            clean(verbose=not args.quiet)
        return 0
    except RuntimeError as e:
        sys.stderr.write(f"ERROR: {e}\n")
        return 1


if __name__ == "__main__":
    main()
