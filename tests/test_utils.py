import importlib
import types
import sys
from pathlib import Path

# Ensure repository root is on the path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest


def test_add_vertical_space(monkeypatch):
    calls = []
    dummy_st = types.SimpleNamespace(sidebar=types.SimpleNamespace(markdown=lambda x: calls.append(x)))
    monkeypatch.setitem(sys.modules, 'streamlit', dummy_st)

    utils = importlib.import_module('utils')
    importlib.reload(utils)

    utils.add_vertical_space(3)
    assert calls == ['---', '---', '---']


def test_ensure_directory(tmp_path):
    import utils
    test_dir = tmp_path / "example"
    utils.ensure_directory(str(test_dir))
    assert test_dir.exists()

    # Should not raise if called again
    utils.ensure_directory(str(test_dir))
    assert test_dir.exists()
