from langchain.document_loaders.csv_loader import CSVLoader


loader = CSVLoader(
    file_path="./data/real_estate_listings.csv",
    source_column="listing",
    csv_args={
        "delimiter": ",", 
        "quotechar": '"',
        "fieldnames": ["neighborhood", "price", "bedrooms", "bathrooms", "house_size", "description", "neighborhood_description", "listing"],
    },
)
# Skip the header row
docs = loader.load()[1:]

docs[0]
