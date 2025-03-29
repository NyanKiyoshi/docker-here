
<div align=center>
<h1><code>docker-here</code></h1>

<img src="https://github.com/user-attachments/assets/3dc11da1-3138-47b8-962a-0a9c0820b68e" width=450 />

Quickly run container images anywhere in the current directory!

</div>

**Contents:**

- [Usage](#usage)
- [Installation](#installation)
- [Demo](#demo)
- [Full Usage](#full-usage)


## Usage

```bash
$ docker-here DOCKER_IMAGE COMMAND
```

Example:

```bash
$ docker-here alpine ls -l
```

## Installation

> [!NOTE]
>
> Only Unix-like systems are supported (Linux, MacOS, etc.).
> **Windows systems are not officially supported.**

Run the following bash script:

```bash
curl --silent -LO https://raw.githubusercontent.com/NyanKiyoshi/docker-here/refs/heads/main/docker-here \
    && mkdir -p ~/.local/bin \
    && mv docker-here ~/.local/bin/ \
    && chmod +x ~/.local/bin/docker-here \
    && { command -v docker-here || echo 'NOTE: you need to add ~/.local/bin/ to your PATH!'; }
```

Alternatively:

1. [Download the docker-here script][download]
2. Put it under ~/.local/bin (or another folder in your `PATH`)
3. Run `chmod +x ~/.local/bin/docker-here`
4. Make sure ~/.local/bin is in your `PATH`

## Demo

```bash
$ docker-here alpine ls -l
total 24
-rw-rw-r--    1 root     root           226 Jan 29 19:22 CONTRIBUTING.md
-rw-rw-r--    1 root     root           100 Jan 29 20:01 README.md
-rwxrwxr-x    1 root     root          4801 Jan 29 19:59 docker-here.sh
drwxrwxr-x    3 root     root          4096 Jan 29 19:27 examples
drwxrwxr-x    4 root     root          4096 Jan 29 20:01 tests

# Are we really running inside a container? Yes!
$ docker-here alpine cat /etc/os-release
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.20.3
PRETTY_NAME="Alpine Linux v3.20"
HOME_URL="https://alpinelinux.org/"
BUG_REPORT_URL="https://gitlab.alpinelinux.org/alpine/aports/-/issues"
```

## Full Usage

```
Usage: docker-here [OPTIONS...] [DOCKER_OPTIONS...] [--] IMAGE [ARGS...]

docker-here - Runs a given container image in a given directory (defaults to current
directory)

OPTIONS
  -s, --src    SRC_PATH   The directory to mount inside the container.
                          Will be mounted under DEST_PATH.

                          Default: $PWD

  -d, --dest   DEST_PATH  The location where the SRC_PATH directory will be
                          mounted inside the remote container.
                          Will be set as the working directory inside the
                          container.

                          Default: $PWD

  --                    Indicates the end of the options for docker-here.

DOCKER OPTIONS
  Any options that unrecognized by 'docker-here' will be forwarded to
  the 'docker-run' command.

  (!) Syntax must be: '--my-option=my-value' - equal signs are required
      for any option that take an argument.

  Examples:
    docker-here --privileged alpine ls
    docker-here --volume=/tmp:/mount-point alpine ls /mount-point
    docker-here --pull=never my-local-image ls

POSITIONAL ARGUMENTS
  IMAGE   The container image to run.
  ARGS    The arguments to pass to 'docker run'.

ENVIRONMENT VARIABLES
  DOCKER_EXE_PATH   The path to the 'docker' command executable (or similar
                    such as podman).

                    Default behavior: automatically detects the command to use.

EXAMPLES
    docker-here alpine ls .
    docker-here alpine sh -uxc 'ls -l "$PWD" ; cat /etc/os-release'
    docker-here alpine --src ~/Downloads -- ls -l .
    docker-here alpine --dest /foo -- ls -l /foo
    docker-here alpine:latest@sha256:d34db33f[...] -- ls -l /foo
    docker-here --volume=/tmp:/mount-point alpline ls -l /mount-point
```

[download]: https://raw.githubusercontent.com/NyanKiyoshi/docker-here/refs/heads/main/docker-here

