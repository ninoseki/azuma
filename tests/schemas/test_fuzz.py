import tempfile
from pathlib import Path

import pytest
from git.repo import Repo

from azuma import schemas
from azuma.exceptions import UnsupportedFeature

# Confirm whether azuma can parse official rules or not


@pytest.fixture(scope="session")
def repo():
    with tempfile.TemporaryDirectory() as dir:
        yield Repo.clone_from("https://github.com/SigmaHQ/sigma", dir)


@pytest.fixture(scope="session")
def paths(repo: Repo):
    dir = Path(repo.working_dir or "")
    return list(dir.glob("./rules/**/*.yml"))


def test_parse_file(paths: list[Path]):
    for path in paths:
        try:
            assert schemas.Rule.parse_file(path).title is not None
        except UnsupportedFeature:
            pass
