"""Final test alphabetically (zz) to catch general integration cases."""

import toml
from test_project import __version__


def test_version():
    """Check that PyProject and __version__ are equivalent."""
    result = toml.load('pyproject.toml')['tool']['poetry']['version']

    assert result == __version__
