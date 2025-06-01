from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st
import sys

# Add the root directory (above 'scripts') to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.interface.pseudo_ui import collect_preferences
from src.search.search_engine import query_real_estate_listings, summarize_listing_results
from src.vector_db.vectorization import populate_vector_db

# Environment setup
try:
    load_dotenv()
except:
    os.environ["OPENAI_API_KEY"] = "<your key here>"
    os.environ["OPENAI_API_BASE"] = ""


def collect_preferences():
    st.title("House Finder 2001")
    st.write("Find your dream home with our personalized search!")

    bedrooms = st.slider("Number of Bedrooms", 1, 10, 3)
    budget_min = st.number_input("Minimum Budget ($)", value=300000)
    budget_max = st.number_input("Maximum Budget ($)", value=500000)
    
    amenities = st.multiselect(
        "Desired Amenities",
        ["Good Schools", "Public Transportation", "Trees", "Garage", "Backyard", "Pool", "Fireplace", "Hardwood Floors", "Open Floor Plan", "Stainless Steel Appliances"],
        default=["Good Schools", "Public Transportation", "Trees"]
    )
    
    neighborhood = st.text_input("Neighborhood Attributes", value="Walkable with parks and restaurants")

    if st.button("Search Listings"):
        return {
            "bedrooms": bedrooms,
            "budget_min": budget_min,
            "budget_max": budget_max,
            "amenities": amenities,
            "neighborhood": neighborhood
        }

    return None

def process_search_results(listings: list):
    """
    Process the search results from the vector database and convert them into a DataFrame for display.
    """
    # Flatten Documents into list of dicts
    flattened = [
        {
            "content": doc.page_content,
            **{f"{k}": v for k, v in doc.metadata.items()}
        }
        for doc in listings
    ]
    # Convert to DataFrame and display
    return pd.DataFrame(flattened)


st.set_page_config(page_title="House Finder 2001")
@st.cache_resource
def load_vector_db():
    return populate_vector_db(file_path="data/real_estate_listings.csv")
db = load_vector_db()

prefs = collect_preferences()
if prefs:
    listings = query_real_estate_listings(db=db, user_preferences=prefs, k=3)
    summary = summarize_listing_results(listing_results=listings, user_preferences=prefs)

    st.subheader("Your Best Matches")
    st.write(summary)

    st.subheader("Result Details")
    df = process_search_results(listings)
    # Display as a more readable table with expandable rows for details
    for idx, row in df.iterrows():
        title = f"{row['neighborhood']} {row['bedrooms']} Bedroom {row['price']}"
        with st.expander(title):
            st.markdown(f"{row['content']}")
