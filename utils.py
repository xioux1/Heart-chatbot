import os
from pathlib import Path
import streamlit as st


def add_vertical_space(spaces: int = 1) -> None:
    """Add vertical space to Streamlit sidebar."""
    for _ in range(spaces):
        st.sidebar.markdown("---")


def ensure_directory(directory: str) -> None:
    """Create directory if it doesn't already exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_model_path(model_filename: str) -> str:
    """Return absolute path to a model in the ``models`` directory."""
    base_dir = Path(__file__).resolve().parent
    return str(base_dir / "models" / model_filename)
