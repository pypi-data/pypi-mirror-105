# precompose_utils

This is a set of tools for working with applications packaged by [precompose](https://github.com/hello-seam/precompose).

## precompose-mount

```
usage: precompose-mount [-h] [--overwrite] [--override-name NAME] REF

Mount a precomposed application

positional arguments:
  REF                   ostree ref to mount

optional arguments:
  -h, --help            show this help message and exit
  --overwrite           overwrite existing app
  --override-name NAME  override app name
```

## precompose-unmount

```
usage: precompose-unmount [-h] [--quiet] [--force] APP

Unmount a precomposed application

positional arguments:
  APP         app to unmount

optional arguments:
  -h, --help  show this help message and exit
  --quiet     suppress output
  --force     ignore running containers
```

## precompose-clean

```
usage: precompose-clean [-h] [--quiet]

Clean up unused checkouts

optional arguments:
  -h, --help  show this help message and exit
  --quiet     suppress output
```
