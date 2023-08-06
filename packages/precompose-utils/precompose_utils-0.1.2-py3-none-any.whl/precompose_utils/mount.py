import argparse
import json
import subprocess
import sys

from pathlib import Path
from typing import List, Optional

from precompose_utils.lockfile import locklib
from precompose_utils.paths import APPS, CHECKOUTS
from precompose_utils.storage import add_storage


@locklib
def mount(
    ref: str, overwrite: bool = False, override_name: Optional[str] = None
) -> Path:
    sha = (
        subprocess.run(["ostree", "rev-parse", ref], check=True, stdout=subprocess.PIPE)
        .stdout.decode()
        .strip()
    )

    metadata = json.loads(
        subprocess.run(
            ["ostree", "cat", ref, "precompose.json"],
            check=True,
            stdout=subprocess.PIPE,
        ).stdout.decode()
    )

    if not isinstance(metadata, dict):
        raise RuntimeError("Invalid precompose.json: not a dict")

    if "precompose" not in metadata:
        raise RuntimeError("Invalid precompose.json: no precompose key")

    if not isinstance(metadata["precompose"], dict):
        raise RuntimeError("Invalid precompose.json: precompose not a dict")

    if "version" not in metadata["precompose"]:
        raise RuntimeError("Invalid precompose.json: no version")

    if not isinstance(metadata["precompose"]["version"], int):
        raise RuntimeError("Invalid precompose.json: version not an int")

    if metadata["precompose"]["version"] > 0:
        raise RuntimeError("Invalid precompose.json: version > 0")

    if "version" not in metadata["precompose"]:
        raise RuntimeError("Invalid precompose.json: no app")

    if not isinstance(metadata["precompose"]["app"], str):
        raise RuntimeError("Invalid precompose.json: version not an int")

    app: str = metadata["precompose"]["app"]
    appdir = APPS.joinpath(app if override_name is None else override_name)

    if appdir.exists():
        if not overwrite:
            sys.stderr.write(f"{app} is already mounted\n")
            return appdir

    if not CHECKOUTS.is_dir():
        CHECKOUTS.mkdir(parents=True)

    sha = (
        subprocess.run(["ostree", "rev-parse", ref], check=True, stdout=subprocess.PIPE)
        .stdout.decode()
        .strip()
    )

    if not CHECKOUTS.is_dir():
        CHECKOUTS.mkdir(parents=True)

    checkout = CHECKOUTS.joinpath(sha)
    if not checkout.exists():
        subprocess.run(["ostree", "checkout", sha, str(checkout)], check=True)

    real_appdir = checkout.joinpath(app)
    if not real_appdir.is_dir():
        raise RuntimeError(f"no app directory ({app}) in {ref}")

    storage = checkout.joinpath("storage")
    if not storage.is_dir():
        raise RuntimeError(f"no storage directory in {ref}")

    add_storage(storage)

    new_appdir = appdir.with_suffix(".new")
    new_appdir.parent.mkdir(parents=True, exist_ok=True)
    new_appdir.symlink_to(real_appdir)
    new_appdir.rename(appdir)

    return appdir


def main(argv: List[str] = sys.argv[1:]) -> int:
    parser = argparse.ArgumentParser(
        prog="precompose-mount",
        description="Mount a precomposed application",
    )
    parser.add_argument("ref", metavar="REF", help="ostree ref to mount")
    parser.add_argument(
        "--overwrite", action="store_true", help="overwrite existing app"
    )
    parser.add_argument("--override-name", metavar="NAME", help="override app name")

    args = parser.parse_args(argv)

    try:
        appdir = mount(
            args.ref, overwrite=args.overwrite, override_name=args.override_name
        )
        print(appdir)
        return 0
    except RuntimeError as e:
        sys.stderr.write(f"ERROR: {e}\n")
        return 1


if __name__ == "__main__":
    main()
