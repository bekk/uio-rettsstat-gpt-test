import config
import os
import openai


from dotenv import load_dotenv, find_dotenv
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import (
    PyPDFLoader,
    DirectoryLoader,
)


def upload():
    try:
        load_status = load_dotenv(find_dotenv())
        print(load_status)
    except Exception as e:
        print(e)
    openai.api_key = os.getenv("OPENAI_API_KEY")

    dir_path = "../data/"

    loader = DirectoryLoader(dir_path, glob="./*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP
    )
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model_kwargs={"device": "mps"})

    VECTORDB = 'vectordb'
    persist_directory = f"embeddings/{VECTORDB}/"

    vectordb = Chroma.from_documents(
        documents=texts, embedding=embeddings, persist_directory=persist_directory
    )

    vectordb.persist()


def main():
    upload()
