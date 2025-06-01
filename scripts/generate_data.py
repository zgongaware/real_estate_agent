import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_generation.data_generator import generate_synthetic_data

if __name__ == "__main__":
    generate_synthetic_data(n=30)



