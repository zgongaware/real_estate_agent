# House Finder 2001

## Overview

House Finder 2001 is a real estate listing application that helps users search, filter, and discover properties for sale or rent. The project aims to simplify the home-finding process with an intuitive interface and powerful search features.

## Features

- Search for houses by location, price, and features
- Filter results by number of bedrooms, bathrooms, and amenities
- View detailed property information

## Project Organization
```
real_estate_agent/
├── scripts/
│   ├── streamlit_app.py        # Main Streamlit application entry point
│   └── generate_data.py        # Script for generating synthetic real estate listing data
├── src/
│   ├── data_generation/
│   │   └── data_generator.py   # Functions for generating synthetic data
│   ├── interface/
│   │   └── pseudo_ui.py        # Functions for collecting user preferences via Streamlit UI
│   ├── search/
│   │   └── search_engine.py    # Functions for performing semantic search on vector database
│   └── vector_db/
│       └── vectorization.py    # Functions for instantiating and populating vector database
├── requirements.txt            # Python package requirements
```

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/zgongaware/real_estate_agent.git
    ```
2. Navigate to the project directory:
    ```bash
    cd real_estate_agent
    ```
3. (Optional) Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Start the application:
    ```bash
    streamlit run scripts/streamlit_app.py # On Windows use: streamlit run scripts\streamlit_app.py
    ```

## Usage

Open your browser and go to `http://localhost:8501/` to start searching for properties.
