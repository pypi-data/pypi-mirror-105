import os

import pytest

from jupyter_core.paths import jupyter_config_path

from jupyter_server.extension.manager import (
    ExtensionPoint,
    ExtensionPackage,
    ExtensionManager,
    ExtensionMetadataError,
    ExtensionModuleNotFound
)

# Use ServerApps environment because it monkeypatches
# jupyter_core.paths and provides a config directory
# that's not cross contaminating the user config directory.
pytestmark = pytest.mark.usefixtures("jp_environ")


def test_extension_point_api():
    # Import mock extension metadata
    from .mockextensions import _jupyter_server_extension_points

    # Testing the first path (which is an extension app).
    metadata_list = _jupyter_server_extension_points()
    point = metadata_list[0]

    module = point["module"]
    app = point["app"]

    e = ExtensionPoint(metadata=point)
    assert e.module_name == module
    assert e.name == app.name
    assert app is not None
    assert callable(e.load)
    assert callable(e.link)
    assert e.validate()


def test_extension_point_metadata_error():
    # Missing the "module" key.
    bad_metadata = {"name": "nonexistent"}
    with pytest.raises(ExtensionMetadataError):
        ExtensionPoint(metadata=bad_metadata)


def test_extension_point_notfound_error():
    bad_metadata = {"module": "nonexistent"}
    with pytest.raises(ExtensionModuleNotFound):
        ExtensionPoint(metadata=bad_metadata)


def test_extension_package_api():
    # Import mock extension metadata
    from .mockextensions import _jupyter_server_extension_points

    # Testing the first path (which is an extension app).
    metadata_list = _jupyter_server_extension_points()
    path1 = metadata_list[0]
    app = path1["app"]

    e = ExtensionPackage(name='jupyter_server.tests.extension.mockextensions')
    e.extension_points
    assert hasattr(e, "extension_points")
    assert len(e.extension_points) == len(metadata_list)
    assert app.name in e.extension_points
    assert e.validate()


def test_extension_package_notfound_error():
    with pytest.raises(ExtensionModuleNotFound):
        ExtensionPackage(name="nonexistent")


def _normalize_path(path_list):
    return [p.rstrip(os.path.sep) for p in path_list]


def test_extension_manager_api():
    jpserver_extensions = {
        "jupyter_server.tests.extension.mockextensions": True
    }
    manager = ExtensionManager()
    assert manager.config_manager
    assert _normalize_path(manager.config_manager.read_config_path) == _normalize_path(jupyter_config_path())
    manager.from_jpserver_extensions(jpserver_extensions)
    assert len(manager.extensions) == 1
    assert "jupyter_server.tests.extension.mockextensions" in manager.extensions


def test_extension_manager_linked_extensions(jp_serverapp):
    name = "jupyter_server.tests.extension.mockextensions"
    manager = ExtensionManager()
    manager.add_extension(name, enabled=True)
    manager.link_extension(name, jp_serverapp)
    assert name in manager.linked_extensions
