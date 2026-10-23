from pathlib import Path

import pytest

from conftest import run_dockerhere


@pytest.mark.parametrize(
    "engine, driver, expected_flags",
    [
        ("docker", None, []),
        ("docker", "journald", []),
        ("podman", None, ["--log-driver=none"]),
        ("podman", "journald", ["--log-driver=journald"]),
    ],
)
def test_log_driver(fake_engine, engine, driver, expected_flags):
    pwd = str(Path(".").absolute())

    fake_engine(engine)

    options = [] if driver is None else ["--podman-log-driver", driver]
    proc = run_dockerhere(*options, "--", "test-image", "echo", "hello")

    assert proc.returncode == 0, proc.stderr.decode()
    args = proc.stdout.decode().splitlines()

    assert args == [
        "run",
        "--rm",
        *expected_flags,
        "-v",
        f"{pwd}:{pwd}",
        "--workdir",
        pwd,
        "test-image",
        "echo",
        "hello",
    ]

    # Shouldn't have put the input args into the 'docker run' command
    # as is
    assert "--podman-log-driver" not in args
    assert "journald" not in args
