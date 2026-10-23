import shutil
import subprocess
from pathlib import Path

import pytest

DOCKER_HERE_PATH = Path(__file__).parent.resolve() / ".." / "docker-here"


def run_dockerhere(*args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [DOCKER_HERE_PATH, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _link_cmd(cmd: str, path: Path) -> None:
    cmd_path = shutil.which(cmd)
    if cmd_path is None:
        raise AssertionError(f"Couldn't find {cmd!r} in PATH")
    (path / cmd).symlink_to(cmd_path)


@pytest.fixture
def fake_engine(tmp_path: Path, monkeypatch):

    def _fake_engine(engine_name: str, set_env: bool = True) -> Path:
        exe = tmp_path / engine_name
        exe.write_text('#!/bin/bash\nprintf "%s\\n" "$@"\n')
        exe.chmod(0o700)
        if set_env:
            # Link needed bash commands so they can be found in the overridden PATH
            _link_cmd("bash", tmp_path)
            _link_cmd("readlink", tmp_path)
            monkeypatch.setenv("PATH", str(tmp_path))
            monkeypatch.delenv("DOCKER_EXE_PATH", raising=False)
        return exe

    yield _fake_engine
