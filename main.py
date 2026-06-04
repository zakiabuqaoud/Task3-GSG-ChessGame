import pandas as pd
import os
import country
import cleaning_pipeline

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

# ===============      Stage 3  ========================

#Q10 What is the win rate for White, Black, and Draw? (% of total games)
print("Q10: What is the win rate for White, Black, and Draw? (% of total games)")
len_chess_df = len(chess_df)
white_win = len((chess_df[chess_df["winner"] == "White"]))
black_win = len((chess_df[chess_df["winner"] == "Black"]))
draw_win = len((chess_df[chess_df["winner"] == "Draw"]))
# Answer: Q10: What is the win rate for White, Black, and Draw?
white_result = (white_win / len_chess_df) * 100
black_result = (black_win / len_chess_df) * 100
draw_result = (draw_win / len_chess_df) * 100
print(f" Q10) white_result: {white_result:.1f}%, black_result:{black_result:.1f}% , draw_result:{draw_result:.1f}%")

#Q11 What is the most common way games end (victory_status)? Resign: 55.6% then Mate, Out of Time,
print("Q11 What is the most common way games end (victory_status)?")
victory_status_with_count = chess_df["victory_status"].value_counts().sort_values(ascending=False)
# print(victory_status_with_count)
# the answer Q11: Resign : 11147
most_vic_res_per = (victory_status_with_count.iloc[0] / len(chess_df)) * 100
print(f"The Q11 Answer: {victory_status_with_count.index[0]}, count: {victory_status_with_count.iloc[0]} => {most_vic_res_per:.1f}%")

#Q12 What is the most common way games end (victory_status)? Resign: 55.6% then Mate, Out of Time,
print("Q12: Victory Status with Highest Average Turns")
avg_turns_by_victory_status = chess_df.groupby('victory_status')['turns'].mean().sort_values(ascending=False)
highest_status = avg_turns_by_victory_status.index[0]
highest_status_per = avg_turns_by_victory_status.iloc[0]
#Answer Q12
print(f"Answer is : {highest_status} Game with {highest_status_per}%")

#Q13 Which opening family is most popular when Black wins? Same for White?
print("Q13: Which opening family is most popular when Black wins? Same for White?")
most_black_win_family_df = chess_df[chess_df["winner"] == "Black"]
most_family_black = most_black_win_family_df["opening_family"].mode()[0]
#Answer Q13
print(f" most black winner Family is {most_family_black}")

# Q14) Do rated games have a different White win rate than unrated games?
# rated white
print("Q14) Do rated games have a different White win rate than unrated games?")
rated_game = chess_df[chess_df["rated"] == True]
rated_white_sum =  len(rated_game[rated_game["winner"] == "White"])
rated_white_rate = (rated_white_sum / len(rated_game)) * 100
# unrated white
unrated_game = chess_df[chess_df["rated"] == False]
unrated_White_sum =  len(unrated_game[unrated_game["winner"]  == "White"])
unrated_White_rate = (unrated_White_sum / len(unrated_game)) * 100
#Answer Q14
print(f"rated games with white winner is {rated_white_rate}%")
print(f"unrated games with White winner is {unrated_White_rate}%")

# Q15: Classify each game as Short/Medium/Long using apply(). What % is each?
print("Classify each game as Short/Medium/Long using apply(). What % is each?")

def find_turn_category_game(turns):
    if turns < 20:
        return 'Short'
    elif turns < 60:
        return 'Medium'
    else:
        return 'Long'

chess_df['turn_category'] = chess_df['turns'].apply(find_turn_category_game)
length_counts = chess_df['turn_category'].value_counts()
turns_cate_percentages = (length_counts / len(chess_df)) * 100
print("Turn category turns_cate_percentages: Answer Q15:")
print(turns_cate_percentages)

# ===============      Stage 4  ========================
# Q16: White players missing from registry?
print("Q16: White players missing from registry?")
white_players = set(chess_df['white_id'].unique())
registered_players = set(players_df['username'].unique())
missing_players = white_players - registered_players
print(f"Answer Q16: Miss White players: {len(missing_players)}")

# Q17: Country Name Inconsistencies"
print("Q17: Country Name Inconsistencies:-")
print(players_df['country'].value_counts())
print(f"Total unique forms: {players_df['country'].nunique()}")
players_df['country_clean'] = players_df['country'].map(country.country_mapping).fillna(players_df['country'])
print(f"the clean country\n {players_df['country_clean'].nunique()} \n {players_df['country_clean'].value_counts()}")


# Q18 - Plot: bar chart of win counts by color. Save to output/wins_by_color.png
print("Q18 - Plot: bar chart is started")
win_counts = chess_df['winner'].value_counts()
win_counts_plot = win_counts.plot(kind='bar', color=['white', 'black', 'gray'], edgecolor='black')
win_counts_plot.get_figure().savefig('output/wins_by_color.png', bbox_inches='tight')
win_counts_plot.get_figure().clf()
print("Q18 - Plot: bar chart is Finished")


# ===============      Cleaning-Pipeline  ========================

cleaned_chess_df = chess_df.pipe(cleaning_pipeline.shaping).pipe(cleaning_pipeline.col_naming_by_snack_case).pipe(cleaning_pipeline.modify_columns_types_chess).pipe(cleaning_pipeline.dealing_with_null).pipe(cleaning_pipeline.dealing_with_invalid_value_chess)
cleaned_player_df = players_df.pipe(cleaning_pipeline.shaping).pipe(cleaning_pipeline.col_naming_by_snack_case).pipe(cleaning_pipeline.modify_columns_types_player).pipe(cleaning_pipeline.dealing_with_null)