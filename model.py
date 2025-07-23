import streamlit as st
import os
from pathlib import Path
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

def main():
    st.set_page_config(
        page_title="Chatbot CSV ChatGPT",
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

    st.title("¿Qué querés saber sobre los pacientes? ❤️")
    st.sidebar.title("About")
    st.sidebar.markdown(
        "Este dataset contiene registros anónimos de pacientes con "
        "enfermedades cardiovasculares. Está pensado para responder preguntas "
        "sobre estos casos clínicos particulares."
    )

    data_path = Path(__file__).resolve().parent / "data" / "heart.csv"
    if not data_path.exists():
        st.error(f"No se encontró el archivo de datos en {data_path}.")
        return

    # El dataset se carga automáticamente para su uso en las consultas

    loader = CSVLoader(file_path=str(data_path), encoding="utf-8", csv_args={'delimiter': ','})
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(data)


    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    docsearch = FAISS.from_documents(text_chunks, embeddings)

    if not os.getenv("OPENAI_API_KEY"):
        st.error("La variable de entorno OPENAI_API_KEY no está configurada.")
        return

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)

    qa = ConversationalRetrievalChain.from_llm(llm, retriever=docsearch.as_retriever())

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    for i, (user_msg, bot_msg) in enumerate(st.session_state["chat_history"]):
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            st.markdown(bot_msg)

    user_input = st.chat_input("Ingresa tu pregunta")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.spinner("Procesando tu pregunta..."):
            result = qa({"question": user_input, "chat_history": st.session_state["chat_history"]})
        bot_answer = result["answer"]
        with st.chat_message("assistant"):
            st.markdown(bot_answer)
        st.session_state["chat_history"].append((user_input, bot_answer))

if __name__ == "__main__":
    main()
