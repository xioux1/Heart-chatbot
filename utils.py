import os
import streamlit as st


def add_vertical_space(spaces: int = 1) -> None:
    """Add vertical space to Streamlit sidebar."""
    for _ in range(spaces):
        st.sidebar.markdown("---")


def ensure_directory(directory: str) -> None:
    """Create directory if it doesn't already exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
