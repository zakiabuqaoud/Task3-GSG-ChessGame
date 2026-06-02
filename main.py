import pandas as pd
import os

# Definition for root variable
url1 = "https://drive.google.com/file/d/1eR3NZtwIC6ECN3vhtrynqmx8okG0twA7/view?usp=sharing"
file_id1 = url1.split("/")[5]
URL1 = f"https://drive.google.com/uc?export=download&id={file_id1}"

url2 = "https://drive.google.com/file/d/1wCSAkGagMzWiToedLC3ZGo_lGf_laF-k/view?usp=sharing"
file_id2 = url2.split("/")[5]
URL2 = f"https://drive.google.com/uc?export=download&id={file_id2}"

# Step 1 : Load Data Set From Internet or local device
def load_data(link, local_path):
    # check Is Data set exist in pc
    if os.path.exists(local_path):
        # loading from local pc and return
        print("loading from local pc...")
        return pd.read_csv(local_path)
    # Downloading from Google Drive...
    print("Downloading from Google Drive...")
    dataframe = pd.read_csv(link)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    dataframe.to_csv(local_path,index = False)
    return dataframe

chess_df = load_data(URL1, "data_raw/chess_games.csv")
players_df = load_data(URL2, "data_raw/player.csv")



