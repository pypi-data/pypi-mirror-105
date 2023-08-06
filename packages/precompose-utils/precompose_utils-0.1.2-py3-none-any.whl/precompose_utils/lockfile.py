import fcntl
import functools

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, TypeVar, cast

from precompose_utils.paths import LIBDIR

_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])


@contextmanager
def lockfile(lockpath: Path):
    with open(lockpath, "a+") as lockfd:
        fcntl.lockf(lockfd, fcntl.LOCK_EX)
        yield


def locked(lockpath: Path):
    def inner(func: _TFunc) -> _TFunc:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            with lockfile(lockpath):
                retval = func(*args, **kwargs)
            return retval

        return cast(_TFunc, wrapper)

    return inner


def locklib(func: _TFunc) -> _TFunc:
    LIBDIR.mkdir(parents=True, exist_ok=True)
    return locked(LIBDIR.joinpath(".precompose.lock"))(func)


def lockstorage(func: _TFunc) -> _TFunc:
    LIBDIR.mkdir(parents=True, exist_ok=True)
    return locked(LIBDIR.joinpath(".storage.lock"))(func)
