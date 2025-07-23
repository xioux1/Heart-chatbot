import streamlit as st
import os
from pathlib import Path
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import ConversationalRetrievalChain

from utils import get_model_path

def main():
    st.set_page_config(
        page_title="Chatbot CSV Llama-2 70B",
        page_icon="❤️",
        layout="centered",
    )

    if hasattr(st, "markdown"):
        st.markdown(
            """
            <style>
                body {
                    background-color: white;
                    font-family: Helvetica, Arial, sans-serif;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    st.title("Chatbot CSV Llama-2 70B ❤️")

    data_path = Path(__file__).resolve().parent / "data" / "heart.csv"
    if not data_path.exists():
        st.error(f"No se encontró el archivo de datos en {data_path}.")
        return

    st.write(f"Usando dataset de ejemplo: {data_path.name}")
    st.write("Procesando el archivo CSV...")

    loader = CSVLoader(file_path=str(data_path), encoding="utf-8", csv_args={'delimiter': ','})
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(data)

    st.write(f"Fragmentos de texto totales: {len(text_chunks)}")

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    docsearch = FAISS.from_documents(text_chunks, embeddings)

    model_path = get_model_path("llama-2-70b-chat.Q2_K.gguf")

    if not os.path.isfile(model_path):
        st.error(
            f"El archivo del modelo no se encontró en {model_path}. Descárguelo como se indica en el README."
        )
        return

    llm = CTransformers(
        model=model_path,
        max_new_tokens=512,
        temperature=0.1,
    )

    qa = ConversationalRetrievalChain.from_llm(llm, retriever=docsearch.as_retriever())

    st.write("Ingresa tu pregunta:")
    query = st.text_input("Pregunta")
    if query:
        with st.spinner("Procesando tu pregunta..."):
            chat_history = []
            result = qa({"question": query, "chat_history": chat_history})
            st.write("Respuesta:", result['answer'])

if __name__ == "__main__":
    main()
