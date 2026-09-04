from load_dataset_module import data_file
from similarity_module import SimilarityCalculator
from user_interface_module import musicSimilarityGUI

# SHU AI Transparency Scale (AITS)
# AITS: 1
# Descriptor: No AI
# Transparency Statement: Artificial Intelligence (AI) has not been used for any part of the activity.
# AI Contributions: AI is not used for any part of the activity.
# Human Contribution: All aspects of the activity are human generated, created, edited, and developed.

def main():
    """
    This main method start by printing message to the user and load
    the data file imported from load_dataset_module, check if no data
    file it will use the sample data I created, print the number of artist
    in the data, proceed to similarity module to create artist feature csv
    file, if anything happen catsh exception could not save data frame.
    finally, start the GUI.
    """
    print("Loading data...")

    # Load data
    data = data_file("data.csv")
    print(data)

    if not data:
        print("No data. Using sample.")
        data = {
            "Artist1": {"Song1": {"danceability": 0.87798, "energy": 0.75463}},
            "Artist2": {"Song2": {"danceability": 0.73452, "energy": 0.61245}},
            "Artist3": {"Song3": {"danceability": 0.56783, "energy": 0.67223}}
        }

    print(f"Loaded {len(data)} artists")

    # Create and save artist dataframe
    calculate = SimilarityCalculator(data)
    try:
        calculate.save_dataframe('artist_features.csv')
        print("Artist features dataframe saved to artist_features.csv")
    except Exception as e:
        print(f"Warning: Could not save dataframe: {e}")

    # Start GUI
    print("Starting GUI...")
    user_interface = musicSimilarityGUI(data)
    user_interface.run()

if __name__ == "__main__":
    main()