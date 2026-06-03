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

# The 2a question ===> Parse time_increment?
print("2a- Parse time_increment?")
time_split = chess_df["time_increment"].str.split('+', expand=True)
chess_df["time_base"] = pd.to_numeric(time_split[0],errors="coerce")
chess_df["time_Sec"] = pd.to_numeric(time_split[1],errors="coerce")

# the answer 2a
print(f"The Answer is:\n {chess_df[['time_increment','time_base', 'time_Sec']]}")

# The 2b question ===> Add rating_diff
print("2b- Add rating_diff: ")
chess_df["rating_diff"] = chess_df["white_rating"] - chess_df["black_rating"]
# the answer 2b
print(f"The Answer 2b is:\n {chess_df['rating_diff']}")

# The 2c question ===> 2c Extract opening_family
print("2c Extract opening_family: ")
chess_df["opening_family"] = chess_df["opening_fullname"].str.split(":").str[0].str.strip()
# the answer 2c
print(f"The Answer 2c is:\n {chess_df[['opening_fullname', 'opening_family']]}")

# 2d : Drop high-null column
print("2d Drop high-null column: ")
print(chess_df.shape)
chess_df = chess_df.drop(columns=['opening_response'])
# the answer 2d
print(chess_df.shape)
print(f"The Answer 2d is: opening_response column is deleted ")

# 2e : Flag short games
print("2e Flag short games: ")
chess_df["is_short"] = chess_df["turns"] < 5
short_games = chess_df[chess_df["is_short"] == True].shape[0]
# the answer 2e
print(f"The Answer 2e is: {short_games} short games ")

# 2f :
print("2f Validate:")
# the answer 2f
assert chess_df['rating_diff'].notna().all(), "rating_diff contain null"
assert chess_df.duplicated().sum() == 0, "There are duplicated"
print("2f validation is Finished.")






