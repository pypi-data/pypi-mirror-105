import os

from pathlib import Path

LIBDIR = Path(
    os.environ.get(
        "PRECOMPOSE_LIBDIR",
        "/sysroot/ostree/precompose"
        if os.path.isdir("/sysroot/ostree")
        else "/var/lib/precompose",
    )
)

APPS = LIBDIR.joinpath("apps")
CHECKOUTS = LIBDIR.joinpath("checkouts")
