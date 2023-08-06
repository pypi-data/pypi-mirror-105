import os.path

import pytest

import appmap._implementation
from appmap._implementation.env import Env
from appmap._implementation.recording import Recorder

def _data_dir(pytestconfig):
    return str(os.path.join(
        str(pytestconfig.rootpath),
        'appmap', 'test', 'data'))

@pytest.fixture(name='data_dir')
def fixture_data_dir(pytestconfig):
    return _data_dir(pytestconfig)

@pytest.fixture(name='with_data_dir')
def fixture_with_data_dir(data_dir, monkeypatch):
    monkeypatch.syspath_prepend(data_dir)
    return data_dir

@pytest.fixture
def events():
    rec = Recorder()
    rec.events().clear()
    rec.enabled = True
    yield rec.events()
    rec.enabled = False
    rec.events().clear()

@pytest.hookimpl
def pytest_runtest_setup(item):
    mark = item.get_closest_marker('appmap_enabled')
    env = {}
    if mark:
        appmap_yml = mark.kwargs.get('config', 'appmap.yml')
        d = _data_dir(item.config)
        config = os.path.join(d, appmap_yml)
        Env.current.set('APPMAP_CONFIG', config)
        env = {'APPMAP': 'true', 'APPMAP_CONFIG': config}

    appmap._implementation.initialize(env=env)  # pylint: disable=protected-access
