from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_chroma import Chroma
import warnings
import shutil
import os

warnings.filterwarnings('ignore')


def create_db(file_URL:str):

    loader = PyPDFLoader(file_path=file_URL)
    pages = loader.load()


    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100,length_function=len,
        is_separator_regex=False)
    chunks = text_splitter.split_documents(pages)
    print(len(chunks))

    ids = [str(i) for i in range(1, len(chunks) + 1)]

    # create the open-source embedding function
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create the Chroma database with IDs
    Chroma.from_documents(pages, embedding_function, persist_directory="app/chroma_db", ids=ids)


def delete_persisted_db():
    db_path = "app/chroma_db"
    if os.path.exists(db_path):
        shutil.rmtree("app/chroma_db")
        print(f"Deleted database and its contents.")
    else:
        print(f"Database does not exist.")



