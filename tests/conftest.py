import os
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


@pytest.fixture
def fake_engine(tmp_path, monkeypatch):
    def _fake_engine(engine_name: str, set_env: bool = True) -> Path:
        exe = tmp_path / engine_name
        exe.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
        exe.chmod(0o700)
        if set_env:
            monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")
        return exe

    yield _fake_engine
