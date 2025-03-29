import pytest
import os
import subprocess
from pathlib import Path, PosixPath


# The default "dummy" image to use in tests.
DEFAULT_IMAGE = "docker.io/alpine:latest"

# The expected default PWD/CWD that docker-here will auto-use.
DEFAULT_PWD = Path(os.getcwd())

# The path to the docker-here executable
DOCKER_HERE_PATH = Path(__file__).parent.resolve() / ".." / "docker-here"


def run_dockerhere(*args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [DOCKER_HERE_PATH, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


@pytest.mark.parametrize(
    "src, dest, expected_pwd",
    [
        # Given,
        #   - src isn't provided
        #   - dest isn't provided
        # Then, the PWD should be used.
        (None, None, DEFAULT_PWD),
        # Given,
        #   - src is the parent directory
        #   - And remote mount destination isn't provided
        # Then, the PWD should be set to 'src'.
        ("..", None, (DEFAULT_PWD / "..").resolve()),
        # Given,
        #   - src isn't provided
        #   - dest is provided
        # Then, src should use PWD, and mount it at 'dest'
        (None, "/foo", PosixPath("/foo")),
    ],
)
def test_mount_paths(src: str | None, dest: str | None, expected_pwd: Path | PosixPath):
    """Ensures the mounting behavior is as expected.

    Checks:
       - The defaults (when --src and/or --dest aren't provided)
       - Provided values (--src, --dest)
    """

    # The script should always use absolute paths, thus we should never
    # expect relative paths (otherwise we may miss issues).
    assert expected_pwd.is_absolute() is True

    # We should never have '..' inside the expected pwd, we expect the script
    # to always normalize the paths.
    assert ".." not in str(expected_pwd)

    args = []
    if src is not None:
        args += ["--src", src]
    if dest is not None:
        args += ["--dest", dest]

    # Prints the PWD
    proc = run_dockerhere(*args, "--", DEFAULT_IMAGE, "pwd")
    assert proc.returncode == 0, f"Command should have succeeded. Stderr: {proc.stderr}"
    assert proc.stdout.decode().strip() == str(expected_pwd)


@pytest.mark.parametrize(
    "args, expected_stdout, is_ok",
    [
        # Given,
        #   - -- is provided (delimits end of named arguments)
        #   - --src is provided
        # Then,
        #   --src shouldn't be parsed by docker-here
        (["--", DEFAULT_IMAGE, "echo", "--src"], "--src", True),  # OK
        # Given,
        #   - -- is provided (delimits end of named arguments)
        #   - --non-existent is provided
        # Then,
        #   --src shouldn't be parsed by docker-here, and thus shouldn't
        #   complain about the option being unknown.
        (["--", DEFAULT_IMAGE, "echo", "--non-existent"], "--non-existent", True),  # OK
        # Given,
        #   - IMAGE is provided (delimits end of named arguments, similar
        #     as the 'docker run' behavior)
        #   - --src is provided
        # Then,
        #   --src shouldn't be parsed by docker-here
        ([DEFAULT_IMAGE, "echo", "--src"], "--src", True),  # OK
        # Given,
        #   - An unrecognized argument (--volume) is provided
        # Then,
        #   --volume should be forwarded to 'docker run'
        (
            ["--volume=.:/mounted", DEFAULT_IMAGE, "sh", "-c", "cd /mounted && pwd"],
            "/mounted",
            True,
        ),  # OK
    ],
)
def test_stops_parsing_arguments(args: list[str], expected_stdout: str, is_ok: bool):
    """Ensures commands are no longer parsed when the user passes "--"
    or as soon as the user provides an image (similarly as the behavior
    of 'docker run').
    """

    # Prints the PWD
    proc = run_dockerhere(*args)

    if is_ok is True:
        assert (
            proc.returncode == 0
        ), f"Command should have succeeded. Stderr: {proc.stderr}"
    else:
        assert (
            proc.returncode == 1
        ), f"Command should have failed. {proc.stderr=} -- {proc.stdout=}"
        assert "Unknown option: --non-existent" in proc.stderr.decode().strip()

    assert proc.stdout.decode().strip() == expected_stdout
