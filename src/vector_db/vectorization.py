from langchain.document_loaders.dataframe import DataFrameLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

import pandas as pd


def populate_vector_db(file_path: str) -> None:
    """
    Populate the vector database with documents from a CSV file.
    """
    # Load documents from the CSV file
    documents = load_documents(file_path = file_path)

    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()

    # Instantiate the Chroma vector store
    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
    )
    return db

   
def load_documents(file_path: str) -> list:
    """
    Load documents from a CSV file and return a list of documents.
    We do this instead of CSVLoader because we want to store the other fields as metadata;
    which isn't yet supported in this version of LangChain.
    """
    dataframe = pd.read_csv(file_path)
    loader = DataFrameLoader(
        data_frame=dataframe,
        page_content_column="listing",
    )
    docs = loader.load()
    return docs