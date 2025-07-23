import importlib
import types
import sys
import os
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


def test_get_model_path(monkeypatch, tmp_path):
    import utils
    dummy_file = tmp_path / "utils.py"
    dummy_file.write_text("")
    monkeypatch.setattr(utils, "__file__", str(dummy_file))

    path = utils.get_model_path("model.gguf")
    expected = tmp_path / "models" / "model.gguf"

    assert os.path.isabs(path)
    assert Path(path) == expected
