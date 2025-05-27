from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

import pandas as pd
import os
import random
import pathlib

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

    # Parse the generated listings into a structured format
    print("Parsing generated listings...")
    results_df = parse_listings(results)

    # Save results to CSV file
    output_path = pathlib.Path("data/real_estate_listings.csv")
    if output_path.exists():
        # Append new results to existing CSV
        existing_df = pd.read_csv(output_path)
        combined_df = pd.concat([existing_df, results_df], ignore_index=True)
    combined_df.to_csv(output_path, index=False)


def generate_prompt_template_base() -> PromptTemplate:
    """
    Generates a LangChain PromptTemplate for creating fictional real estate listings.
    The template includes placeholders for neighborhood, price, bedrooms, bathrooms, house size, and descriptions.
    Returns:
        PromptTemplate: A LangChain PromptTemplate object containing the prompt structure for real estate listings.
    """
    prompt_template_str = """
    Generate a fictional real estate listing with the following structure:

    Neighborhood: {neighborhood}
    Price: ${price}
    Bedrooms: {bedrooms}
    Bathrooms: {bathrooms}
    House Size: {size} sqft
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
    Neighborhood: {neighborhood}
    Price: ${price}
    Bedrooms: {bedrooms}
    Bathrooms: {bathrooms}
    House Size: {size} sqft
    Description:
    Neighborhood Description:
    """
    return PromptTemplate(
        input_variables=["neighborhood", "price", "bedrooms", "bathrooms", "size"],
        template=prompt_template_str
    )


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
    filled_prompt = template.format(**seed)
    response = model.predict(filled_prompt)
    return response.strip()


def parse_listings(results: list) -> pd.DataFrame:

    # Convert list of listings to a DataFrame
    listings = pd.DataFrame(results, columns=["listing"])

    # Split each row by newlines, then split each line by colon to get key-value pairs for all rows
    parsed_rows = listings.iloc[:, 0].apply(parse_row)
    parsed_df = pd.DataFrame(parsed_rows.tolist())
    
    # Clean up the DataFrame
    parsed_df["Description"] = parsed_df["Description"].apply(lambda x: pd.NA if x == "" else x)
    parsed_df["Neighborhood Description"] = parsed_df["Neighborhood Description"].apply(lambda x: pd.NA if x == "" else x)
    parsed_df.dropna(axis=0, how="any", inplace=True)

    # Merge full listing back into the DataFrame
    final_df = parsed_df.merge(listings, left_index=True, right_index=True, suffixes=("", "_original"), how="left")
    final_df.columns = final_df.columns.str.lower().str.replace(" ", "_")

    return final_df


def parse_row(row):
    """
    Parses a single row of text into a dictionary of key-value pairs.
    """
    lines = row.split("\n")
    key_value_pairs = [line.split(":", 1) for line in lines if ":" in line]
    return {k.strip(): v.strip() for k, v in key_value_pairs}