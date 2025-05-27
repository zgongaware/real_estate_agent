from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from jinja2 import Template

import pandas as pd
import os
import random
import re
import pathlib
import pickle

try:
    load_dotenv()
except:
    os.environ["OPENAI_API_KEY"] = "<your key here>"
    os.environ["OPENAI_API_BASE"] = ""


def generate_synthetic_data(n: int = 25) -> None:
    """
    Generates synthetic real estate listings using a language model and saves them to a CSV file.
    The listings include details such as neighborhood, price, bedrooms, bathrooms, house size, and descriptions.
    """
    # Instantiate LLM
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.9, max_tokens=2000)

    # Iterate to generate multiple listings
    results = []
    for _ in range(n):
        print(f"Generating listing {_ + 1} of {n}...")
        seed = generate_listing_seed()
        full_output = generate_listing(seed=seed, model=llm)
        results.append(full_output)

    # Save results to pickle file
    output_path = pathlib.Path("data/real_estate_listings.pkl")
    if output_path.exists():
        # Load existing data and append new results
        with open(output_path, "rb") as f:
            existing_results = pickle.load(f)
        all_results = existing_results + results
    else:
        all_results = results

    with open(output_path, "wb") as f:
        pickle.dump(all_results, f)


def generate_prompt_template_base() -> Template:
    """
    Generates a Jinja2 template string for creating fictional real estate listings.
    The template includes placeholders for neighborhood, price, bedrooms, bathrooms, house size, and descriptions.
    It provides an example listing and instructs the user to generate a new listing with vivid and realistic details.
    Returns:
        Template: A Jinja2 Template object containing the prompt structure for real estate listings.
    """        
    # Define prompt template
    prompt_template_str = """
        Generate a fictional real estate listing with the following structure:

        Neighborhood: {{ neighborhood }}
        Price: ${{ price }}
        Bedrooms: {{ bedrooms }}
        Bathrooms: {{ bathrooms }}
        House Size: {{ size }} sqft
        Description: 
        Neighborhood Description:

        Ensure the home description is vivid, realistic, and reflects the number of rooms and the character of the neighborhood.

        Example:
        ***
        Neighborhood: Green Oaks
        Price: $800,000
        Bedrooms: 3
        Bathrooms: 2
        House Size: 2,000 sqft
        Description: Welcome to this eco-friendly oasis nestled in the heart of Green Oaks...
        Neighborhood Description: Green Oaks is a close-knit, environmentally-conscious community...
        ***

        Now generate a new fictional listing:
        ***
        Neighborhood: {{ neighborhood }}
        Price: ${{ price }}
        Bedrooms: {{ bedrooms }}
        Bathrooms: {{ bathrooms }}
        House Size: {{ size }} sqft
        Description:
        Neighborhood Description:
    """
    return Template(prompt_template_str)


def generate_listing_seed() -> dict:
    """
    Randomly selects a neighborhood, generates random values for price, bedrooms, bathrooms,
    house size, and returns them in a dictionary format.
    """
    neighborhoods = [
        "Willow Ridge", "Oceanview Heights", "Sunnyvale", "Maplewood", "Highland Pines",
        "Cedar Bluff", "Silverbrook", "Stonegate", "Meadow Hills", "Fox Hollow"
    ]
    nhood = random.choice(neighborhoods)
    bedrooms = random.randint(2, 5)
    bathrooms = random.randint(1, 4)
    size = random.randint(1200, 3500)
    price = random.randint(300_000, 1_200_000)
    return {
        "neighborhood": nhood,
        "price": price,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "size": size
    }


def generate_listing(seed: dict, model: OpenAI) -> str:
    """
    Generates a real estate listing using a prompt template and a language model.
    Fills the template with the provided seed data and returns the full text of the listing.
    """
    template = generate_prompt_template_base()
    filled_prompt = template.render(**seed)
    response = model.predict(filled_prompt)
    return response.strip()


def load_real_estate_listings(filepath='real_estate_listings.pkle'):
    """
    Loads real estate listings from a pickle file.
    """
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    return data