import contextlib
import tempfile
from pathlib import Path

import ci
import pytest
from git.repo import Repo

from azuma import schemas
from azuma.exceptions import UnsupportedFeatureError

# Confirm whether azuma can parse official rules or not


@pytest.fixture(scope="session")
def repo():
    with tempfile.TemporaryDirectory() as dir:
        yield Repo.clone_from("https://github.com/SigmaHQ/sigma", dir)


@pytest.fixture(scope="session")
def paths(repo: Repo):
    dir = Path(repo.working_dir or "")
    return list(dir.glob("./rules/**/*.yml"))


@pytest.mark.skipif(not ci.is_ci(), reason="do fuzzing test in CI")
def test_parse_file(paths: list[Path]):
    for path in paths:
        with contextlib.suppress(UnsupportedFeatureError):
            assert schemas.Rule.model_validate_file(path).title is not None
