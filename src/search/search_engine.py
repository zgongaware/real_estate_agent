from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.vectorstores import Chroma

import os

try:
    load_dotenv()
except:
    os.environ["OPENAI_API_KEY"] = "<your key here>"
    os.environ["OPENAI_API_BASE"] = ""


def define_retriever_helper(db: Chroma) -> SelfQueryRetriever:
    """
    Defines a retriever for querying real estate listings from a vector database.
    This function sets up the metadata fields and the LLM to be used for retrieval.
    """
    metadata_fields = [
        AttributeInfo(name="neighborhood", description="The neighborhood where the property is located.", type="string"),
        AttributeInfo(name="price", description="The price of the property in USD.", type="string"),
        AttributeInfo(name="bedrooms", description="The number of bedrooms in the property.", type="string"),
        AttributeInfo(name="bathrooms", description="The number of bathrooms in the property.", type="string"),
        AttributeInfo(name="size", description="The size of the property in square feet.", type="string"),
        AttributeInfo(name="description", description="A brief description of the property.", type="string"),
        AttributeInfo(name="neighborhood_description", description="A description of the neighborhood where the property is located.", type="string")
    ]
    document_content_description = "A real estate listing containing details about a property, including neighborhood, price, bedrooms, bathrooms, size, and description."
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0)
    
    return SelfQueryRetriever.from_llm(
        llm, db, document_content_description, metadata_fields
    )

