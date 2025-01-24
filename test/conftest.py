import os
import shutil

import pytest


@pytest.fixture
def wildcards_directory(tmpdir):
    src = os.path.join(os.path.dirname(__file__), "fixtures/wildcards")
    dest = tmpdir.mkdir("wildcards")
    shutil.copytree(src, str(dest), dirs_exist_ok=True)
    return dest


@pytest.fixture
def tweaks_directory(tmpdir):
    src = os.path.join(os.path.dirname(__file__), "fixtures/tweaks")
    dest = tmpdir.mkdir("tweaks")
    shutil.copytree(src, str(dest), dirs_exist_ok=True)
    return dest


@pytest.fixture
def models_directory(tmpdir):
    src = os.path.join(os.path.dirname(__file__), "fixtures/models")
    dest = tmpdir.mkdir("models")
    shutil.copytree(src, str(dest), dirs_exist_ok=True)
    return dest
