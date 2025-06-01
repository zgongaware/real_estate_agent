import streamlit as st

def collect_preferences():
    st.title("Real Estate Search Preferences")

    bedrooms = st.slider("Number of Bedrooms", 1, 10, 3)
    budget_min = st.number_input("Minimum Budget ($)", value=300000)
    budget_max = st.number_input("Maximum Budget ($)", value=500000)
    
    amenities = st.multiselect(
        "Desired Amenities",
        ["Good Schools", "Public Transportation", "Trees", "Garage", "Backyard", "Pool"],
        default=["Good Schools", "Public Transportation", "Trees"]
    )
    
    neighborhood = st.text_input("Neighborhood Description", value="Walkable with parks and restaurants")

    if st.button("Search Listings"):
        return {
            "bedrooms": bedrooms,
            "budget_min": budget_min,
            "budget_max": budget_max,
            "amenities": amenities,
            "neighborhood": neighborhood
        }

    return None