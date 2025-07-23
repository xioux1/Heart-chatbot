import sys
import types
from pathlib import Path
import importlib

# Ensure repository root is on the path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest


def test_main_missing_model(monkeypatch, tmp_path):
    # Prepare dummy Streamlit
    calls = {"error": []}
    dummy_file = types.SimpleNamespace(name="file.csv", getvalue=lambda: b"a,b\n1,2")
    dummy_sidebar = types.SimpleNamespace(
        title=lambda x: None,
        markdown=lambda x: None,
        file_uploader=lambda label, type=None: dummy_file,
        write=lambda x: None,
    )
    dummy_st = types.SimpleNamespace(
        set_page_config=lambda **kwargs: None,
        title=lambda x: None,
        sidebar=dummy_sidebar,
        write=lambda x: None,
        error=lambda x: calls["error"].append(x),
        text_input=lambda prompt: "",
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

    class DummyLLM:
        pass

    class DummyChain:
        @staticmethod
        def from_llm(llm, retriever=None):
            return None

    # Build fake langchain package structure
    langchain = types.ModuleType("langchain")
    langchain.document_loaders = types.ModuleType("document_loaders")
    langchain.document_loaders.csv_loader = types.ModuleType("csv_loader")
    langchain.document_loaders.csv_loader.CSVLoader = DummyLoader
    langchain.text_splitter = types.ModuleType("text_splitter")
    langchain.text_splitter.RecursiveCharacterTextSplitter = DummySplitter
    langchain.embeddings = types.ModuleType("embeddings")
    langchain.embeddings.HuggingFaceEmbeddings = DummyEmbeddings
    langchain.vectorstores = types.ModuleType("vectorstores")
    langchain.vectorstores.FAISS = DummyFAISS
    langchain.llms = types.ModuleType("llms")
    langchain.llms.CTransformers = DummyLLM
    langchain.chains = types.ModuleType("chains")
    langchain.chains.ConversationalRetrievalChain = DummyChain

    monkeypatch.setitem(sys.modules, "langchain", langchain)
    monkeypatch.setitem(sys.modules, "langchain.document_loaders", langchain.document_loaders)
    monkeypatch.setitem(sys.modules, "langchain.document_loaders.csv_loader", langchain.document_loaders.csv_loader)
    monkeypatch.setitem(sys.modules, "langchain.text_splitter", langchain.text_splitter)
    monkeypatch.setitem(sys.modules, "langchain.embeddings", langchain.embeddings)
    monkeypatch.setitem(sys.modules, "langchain.vectorstores", langchain.vectorstores)
    monkeypatch.setitem(sys.modules, "langchain.llms", langchain.llms)
    monkeypatch.setitem(sys.modules, "langchain.chains", langchain.chains)

    monkeypatch.chdir(tmp_path)

    # Import model with our dummy modules
    model = importlib.import_module("model")
    importlib.reload(model)

    # Replace get_model_path and isfile to trigger error branch
    monkeypatch.setattr(model, "get_model_path", lambda name: str(tmp_path / name))
    monkeypatch.setattr(model.os.path, "isfile", lambda path: False)

    model.main()

    # File written from upload
    written = tmp_path / "temp" / "file.csv"
    assert written.exists()
    assert written.read_bytes() == b"a,b\n1,2"

    # Loader invoked with written file
    assert DummyLoader.called == str(Path("temp") / "file.csv")

    # Error displayed when model missing
    assert calls["error"], "Expected error message when model file is missing"
    assert "Model file not found" in calls["error"][0]
