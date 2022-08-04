import sys
from . import brew_file
from pathlib import Path
import pytest
import os


def test_is_mac():
    assert (bool(sys.platform == 'darwin') == bool(brew_file.is_mac()))


@pytest.mark.parametrize(
    "val, result",
    [(True, True), (False, False), (0, False), (1, True), (10, True), ('true', True), ('false', False), ('others', False)]
)
def test_to_bool(val, result):
    ret = brew_file.to_bool(val)
    assert type(ret) == bool
    assert ret == result


@pytest.mark.parametrize(
    "val, result",
    [(True, 1), (False, 0), (1, 1), ('1', 1), ('01', 1), ('true', 1), ('false', 0), ('others', 0)]
)
def test_to_num(val, result):
    ret = brew_file.to_num(val)
    assert type(ret) == int
    assert ret == result


@pytest.mark.parametrize(
    "path, result",
    [
        ("/normal/path", "/normal/path"),
        ("${HOSTNAME}/$HOSTTYPE/${OSTYPE}/$PLATFORM", f"{brew_file.shell_envs['HOSTNAME']}/{brew_file.shell_envs['HOSTTYPE']}/{brew_file.shell_envs['OSTYPE']}/{brew_file.shell_envs['PLATFORM']}"),
        ("~/test", os.path.expanduser("~/test")),
        ("$HOME/", os.path.expanduser("~/")),
        ("${HOME}/", os.path.expanduser("~/")),
    ]
)
def test_expandpath(path, result):
    assert brew_file.expandpath(path) == Path(result)
