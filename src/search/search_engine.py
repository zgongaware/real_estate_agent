from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma


import os

try:
    load_dotenv()
except:
    os.environ["OPENAI_API_KEY"] = "<your key here>"
    os.environ["OPENAI_API_BASE"] = ""


def summarize_listing_results(listing_results: list, user_preferences: dict) -> str:
    """
    Based on the real estate listings returned from the vector database, 
    create a personalized summary of each listing based on the user's preferences.
    """
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0)
    query = f"""Given the user's user preferences: {user_preferences}\n and the following real estate listings: {listing_results}\ngenerate a personalized summary of each listing that highlights how well it matches the user's preferences. Each summary should be concise and focus on the key features that align with the user's needs, and be no longer than 2 sentences."""
    summary = llm(query)
    return "We've found the following listings that match your preferences:\n" + summary


def query_real_estate_listings(db: Chroma, user_preferences: dict, k: int = 3) -> list:
    """
    Query the vector database for real estate listings based on user preferences.
    Ensures only unique listings are returned.
    """
    query = (
        f"{user_preferences['bedrooms']} bedroom homes, priced between "
        f"${user_preferences['budget_min']} and ${user_preferences['budget_max']}, "
        f"located in walkable neighborhoods with amenities like "
        f"{', '.join(user_preferences['amenities'])}"
    )
    results = db.similarity_search(query, k=k*2)  # Fetch extra in case of duplicates
    unique = []
    seen = set()
    for listing in results:
        # Use the string representation of the listing for uniqueness
        identifier = str(listing)
        if identifier not in seen:
            unique.append(listing)
            seen.add(identifier)
        if len(unique) == k:
            break
    return unique


def precompose_user_preferences() -> dict:
    return {
        "bedrooms": 3,
        "budget_min": 300000,
        "budget_max": 500000,
        "amenities": ["Good Schools", "Public Transportation", "Trees"],
        "neighborhood": "Walkable with parks and restaurants"
    }
