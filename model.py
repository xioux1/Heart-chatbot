import streamlit as st
import os
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain_community.chains import ConversationalRetrievalChain

from utils import add_vertical_space, ensure_directory, get_model_path

def main():
    st.set_page_config(page_title="Phi-3 Mini CSV Chatbot")
    st.title("Phi-3 Mini CSV Chatbot")

    st.sidebar.title("About")
    st.sidebar.markdown('''
        The Phi-3 Mini CSV Chatbot uses the **Phi-3 Mini 3.8B** model.
        
        ### 🔄Bot evolving, stay tuned!
        
        ## Useful Links 🔗
        
        - **Model:** [Phi-3 Mini 3.8B](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-GGUF) 📚
        - **GitHub:** [ThisIs-Developer/Llama-2-GGML-CSV-Chatbot](https://github.com/ThisIs-Developer/Llama-2-GGML-CSV-Chatbot) 💬
    ''')

    TEMP_DIR = "temp"

    ensure_directory(TEMP_DIR)

    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])

    add_vertical_space(1)
    st.sidebar.write('Made by [@ThisIs-Developer](https://huggingface.co/ThisIs-Developer)')

    if uploaded_file is not None:
        file_path = os.path.join(TEMP_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        st.write(f"Uploaded file: {uploaded_file.name}")
        st.write("Processing CSV file...")

        loader = CSVLoader(file_path=file_path, encoding="utf-8", csv_args={'delimiter': ','})
        data = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        text_chunks = text_splitter.split_documents(data)

        st.write(f"Total text chunks: {len(text_chunks)}")

        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        docsearch = FAISS.from_documents(text_chunks, embeddings)

        model_path = get_model_path("Phi-3-mini-4k-instruct-q4.gguf")

        if not os.path.isfile(model_path):
            st.error(
                f"Model file not found at {model_path}. Please download it as"
                " described in the README."
            )
            return

        llm = CTransformers(model=model_path,
                            model_type="phi3",
                            max_new_tokens=512,
                            temperature=0.1)

        qa = ConversationalRetrievalChain.from_llm(llm, retriever=docsearch.as_retriever())

        st.write("Enter your query:")
        query = st.text_input("Input Prompt:")
        if query:
            with st.spinner("Processing your question..."):
                chat_history = []
                result = qa({"question": query, "chat_history": chat_history})
                st.write("Response:", result['answer'])

        os.remove(file_path)

if __name__ == "__main__":
    main()
