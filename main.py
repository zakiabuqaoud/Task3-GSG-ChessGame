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
# print(chess_df)
# print(players_df)

# ===============      Stage 1 ========================

# The 1st question
print("1- How many records are in the dataset?")
# the answer is 20058 rows
print(f"The Answer is: {chess_df.shape[0]} rows")

# The 2nd question
print("2- How many exact duplicate rows exist?")
# the answer is 0 exact duplicates
print(f"The Answer is: {chess_df.duplicated().sum()} exact duplicates")

# The 3rd question
print("3- How many games have duplicate move sequences?")
# the answer is 1138 duplicates
print(f"The Answer is: {chess_df.duplicated(subset=['moves']).sum()} duplicates")

# The 4th question
print("4- What % of opening_response is missing?")
missing_open_response_count = chess_df['opening_response'].isna().sum()
miss_open_res_result = (missing_open_response_count / len(chess_df)) * 100
# the answer is 93.982450892412%
print(f"The Answer is: {miss_open_res_result}%")

# The 5th question
print("5- What % of opening_variation is missing?")
missing_open_var_count = chess_df['opening_variation'].isna().sum()
miss_open_var_result = (missing_open_var_count / len(chess_df)) * 100
# the answer is % 28.218167314787117%
print(f"The Answer is: {miss_open_var_result}%")

# The 6th question
print("6- What is the minimum number of turns in any game? Why is this suspicious?")
min_turns = chess_df['turns'].min()
# the answer is 1
print(f"The Answer is: {min_turns}")


# ===============      Stage 2  ========================










