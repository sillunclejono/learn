import os
import sys
from importlib import import_module

# ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_app_importable():
    try:
        app = import_module('app')
        assert hasattr(app, 'app')
    except Exception as e:
        raise AssertionError(f'Failed to import app: {e}')
