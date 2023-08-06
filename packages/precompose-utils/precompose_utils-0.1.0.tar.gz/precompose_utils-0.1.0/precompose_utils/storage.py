import sys
import toml

from pathlib import Path
from typing import Any, MutableMapping

from precompose_utils.lockfile import lockstorage

STORAGE_CONF = Path("/etc/containers/storage.conf")


def _load_config():
    with open(STORAGE_CONF, "r") as conf_in:
        config = toml.load(conf_in)
        if "storage" not in config:
            config["storage"] = {}

        if "options" not in config["storage"]:
            config["storage"]["options"] = {}

        if "additionalimagestores" not in config["storage"]["options"]:
            config["storage"]["options"]["additionalimagestores"] = []

        return config


def _write_config(config: MutableMapping[str, Any]):
    backup = STORAGE_CONF.with_suffix(".bak")
    if backup.exists():
        backup.unlink()
    STORAGE_CONF.link_to(backup)

    new_STORAGE_CONF = STORAGE_CONF.with_suffix(".new")
    with open(new_STORAGE_CONF, "w") as conf_out:
        toml.dump(config, conf_out)

    new_STORAGE_CONF.rename(STORAGE_CONF)


@lockstorage
def add_storage(storage: Path, verbose: bool = False):
    config = _load_config()
    if str(storage) not in config["storage"]["options"]["additionalimagestores"]:
        if verbose:
            sys.stderr.write(f"Adding {storage} to storage.conf ...")
        config["storage"]["options"]["additionalimagestores"].append(str(storage))
        _write_config(config)


@lockstorage
def remove_storage(storage: Path, verbose: bool = False):
    config = _load_config()
    if str(storage) in config["storage"]["options"]["additionalimagestores"]:
        if verbose:
            sys.stderr.write(f"Removing {storage} from storage.conf ...\n")
        config["storage"]["options"]["additionalimagestores"].remove(str(storage))
        _write_config(config)


@lockstorage
def remove_missing_storage(verbose: bool = False):
    config = _load_config()
    changed = False
    for s in config["storage"]["options"]["additionalimagestores"]:
        storage = Path(str(s))
        if not storage.is_dir():
            if verbose:
                sys.stderr.write(f"Removing missing {storage} from storage.conf ...\n")
            config["storage"]["options"]["additionalimagestores"].remove(str(storage))
            changed = True

    if changed:
        _write_config(config)
