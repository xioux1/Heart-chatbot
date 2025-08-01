import sys
import types
from pathlib import Path
import importlib

# Ensure repository root is on the path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest


def test_main_missing_api_key(monkeypatch, tmp_path):
    # Prepare dummy Streamlit
    calls = {"error": []}
    dummy_sidebar = types.SimpleNamespace(
        title=lambda x: None,
        markdown=lambda x: None,
        write=lambda x: None,
    )
    dummy_st = types.SimpleNamespace(
        set_page_config=lambda **kwargs: None,
        title=lambda x: None,
        sidebar=dummy_sidebar,
        write=lambda x: None,
        error=lambda x: calls["error"].append(x),
        chat_input=lambda prompt: "",
        chat_message=lambda role: types.SimpleNamespace(markdown=lambda content: None),
        spinner=lambda text: types.SimpleNamespace(__enter__=lambda self: None, __exit__=lambda self, exc_type, exc, tb: None),
    )
    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)

    # Dummy langchain components to avoid heavy imports
    class DummyLoader:
        def __init__(self, file_path, encoding="utf-8", csv_args=None):
            DummyLoader.called = file_path
        def load(self):
            return ["doc"]
    DummyLoader.called = None

    class DummySplitter:
        def __init__(self, *a, **k):
            pass
        def split_documents(self, data):
            return ["chunk"]

    class DummyEmbeddings:
        def __init__(self, model_name):
            self.model_name = model_name

    class DummyDocsearch:
        def __init__(self, docs, emb):
            self.docs = docs
            self.emb = emb
        def save_local(self, path):
            self.saved = path
        def as_retriever(self):
            return "retriever"
    class DummyFAISS:
        @staticmethod
        def from_documents(docs, emb):
            return DummyDocsearch(docs, emb)

    class DummyChat:
        def __init__(self, *a, **k):
            pass

    class DummyChain:
        @staticmethod
        def from_llm(llm, retriever=None):
            return None

    # Build fake langchain_community package structure
    lc_comm = types.ModuleType("langchain_community")
    lc_comm.document_loaders = types.ModuleType("document_loaders")
    lc_comm.document_loaders.csv_loader = types.ModuleType("csv_loader")
    lc_comm.document_loaders.csv_loader.CSVLoader = DummyLoader
    lc_comm.embeddings = types.ModuleType("embeddings")
    lc_comm.embeddings.HuggingFaceEmbeddings = DummyEmbeddings
    lc_comm.vectorstores = types.ModuleType("vectorstores")
    lc_comm.vectorstores.FAISS = DummyFAISS
    lc_openai = types.ModuleType("langchain_openai")
    lc_openai.ChatOpenAI = DummyChat
    lc_comm.chains = types.ModuleType("chains")
    lc_comm.chains.ConversationalRetrievalChain = DummyChain

    # Build fake langchain package with generic chains
    lc_main = types.ModuleType("langchain")
    lc_main.chains = types.ModuleType("chains")
    lc_main.chains.ConversationalRetrievalChain = DummyChain

    # Dummy text_splitters module
    lc_splitters = types.ModuleType("langchain_text_splitters")
    lc_splitters.RecursiveCharacterTextSplitter = DummySplitter

    monkeypatch.setitem(sys.modules, "langchain_community", lc_comm)
    monkeypatch.setitem(sys.modules, "langchain_community.document_loaders", lc_comm.document_loaders)
    monkeypatch.setitem(sys.modules, "langchain_community.document_loaders.csv_loader", lc_comm.document_loaders.csv_loader)
    monkeypatch.setitem(sys.modules, "langchain_community.embeddings", lc_comm.embeddings)
    monkeypatch.setitem(sys.modules, "langchain_community.vectorstores", lc_comm.vectorstores)
    monkeypatch.setitem(sys.modules, "langchain_openai", lc_openai)
    monkeypatch.setitem(sys.modules, "langchain_community.chains", lc_comm.chains)
    monkeypatch.setitem(sys.modules, "langchain", lc_main)
    monkeypatch.setitem(sys.modules, "langchain.chains", lc_main.chains)
    monkeypatch.setitem(sys.modules, "langchain_text_splitters", lc_splitters)

    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    # Import model with our dummy modules
    model = importlib.import_module("model")
    importlib.reload(model)

    model.main()

    expected_dataset = Path(model.__file__).resolve().parent / "data" / "heart.csv"

    # Loader invoked with dataset file
    assert DummyLoader.called == str(expected_dataset)

    # Error displayed when API key missing
    assert calls["error"], "Expected error message when API key is missing"
    assert "OPENAI_API_KEY" in calls["error"][0]
