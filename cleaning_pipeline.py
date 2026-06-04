import pandas as pd
from pandas import DataFrame
import re
import columns_with_target_types
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# Step 2: Shaping
def shaping(df_loaded: DataFrame):
    print("Step2: Shaping Started:-")
    # view shape old dataframe
    print("old shape:", df_loaded.shape)

    # remove all row contains empty in all cells
    df_shaped = df_loaded.dropna(how = "all")

    # remove columns contain on most null
    if "opening_response" in df_loaded.columns:
        df_loaded = df_loaded.drop(columns=['opening_response'])
    logging.info(f"new Shape: {df_loaded.shape}")
    print("new shape:", df_loaded.shape)
    print("step2: shaping function finished")
    return df_loaded

# Step 3: Shaping
def col_naming_by_snack_case(df_shaped):
    # changing in column names amd make it by snack case
    print(" step3: col naming function started")
    new_naming_col = []
    print(f"old naming :\n {df_shaped.columns}")
    for col_name in df_shaped.columns:
        # replace from space to underscore and remove  [()]
        target_str = re.sub(r"\s+", "_", str(col_name).strip())
        target_str = re.sub(r'[()]', '', target_str)
        target_str = target_str.lower()
        new_naming_col.append(target_str)
    df_shaped.columns = new_naming_col
    # print(df_shaped.columns )
    print(f"new naming :\n {df_shaped.columns}")
    print(" step3: col naming function finished")
    return df_shaped

# Step 4: Type chess
def modify_columns_types_chess(df_col_nemed):
    print("Step4: Type Step Started For Chess Matches")
    print(f"old types is \n {df_col_nemed.dtypes}" )
    for col_name, t in columns_with_target_types.target_type_columns_chess.items():
        if t == "category" or t == "string":
            df_col_nemed[col_name] = df_col_nemed[col_name].astype(t)
        if t == "Int64":
            df_col_nemed[col_name] = pd.to_numeric(df_col_nemed[col_name], errors="coerce")
        if t == "boolean":
            df_col_nemed[col_name] = df_col_nemed[col_name].map({'Y': True, 'N': False, 'y': True, 'n': False})
            df_col_nemed[col_name] = df_col_nemed[col_name].astype(t)
    print(f"New Types is \n {df_col_nemed.dtypes}")
    logging.info("change col type to target type:-")
    print("step 4: type columns finished For Chess Matches")
    return df_col_nemed

# Step 4: type player
def modify_columns_types_player(df_col_nemed):
    print("Step4: Type Step Started For Players")
    print(f"old types is \n {df_col_nemed.dtypes}" )
    for col_name, t in columns_with_target_types.target_type_columns_player.items():
        if t == "category" or t == "string":
            df_col_nemed = df_col_nemed.fillna({
                col_name: "unknown",
            })
            df_col_nemed[col_name] = df_col_nemed[col_name].astype(t)
        if t == "Int64":
            df_col_nemed[col_name] = pd.to_numeric(df_col_nemed[col_name], errors="coerce")
        if t == "boolean":
            df_col_nemed[col_name] = df_col_nemed[col_name].map({'Y': True, 'N': False, 'y': True, 'n': False})
            df_col_nemed[col_name] = df_col_nemed[col_name].astype(t)
    print(f"New Types is \n {df_col_nemed.dtypes}")
    print("step 4: type columns finished For Players")
    return df_col_nemed

# Step 5: Remove Nulls
def dealing_with_null(df_typed):
    print("Step 5: Dealing With Null Started :-")
    # print(df_typed.isnull().sum())
    # drop row which contain null in column [rated]
    if "rated" in df_typed:
        df_typed = df_typed.dropna(subset=["rated"])
    logging.info("treat nulls: rows deleted that contain null in rated")
    # # fill null [opening_variation]
    if "opening_variation" in df_typed:
        df_typed = df_typed.fillna({
            "opening_variation": "unknown",
        })
    # # fill null [country]
    if "country" in df_typed:
            df_typed = df_typed.fillna({
                "country": "unknown",
            })
    if "country_clean" in df_typed:
        df_typed = df_typed.fillna({
            "country_clean": "unknown",
        })
    logging.info("treat nulls: fill missing value in country and country_clean")


    print("After Removed Null:-")
    print(df_typed.isnull().sum())
    print("step 5: Dealing and treat null : Finished")
    return df_typed

# step 6: Dealing With invalid value in chess
def dealing_with_invalid_value_chess(df_not_null):
    print("step 6: repair invalid value is started for chess:-")
    # clean invalid value in rating
    for col in ['white_rating', 'black_rating']:
        invalid = (df_not_null[col] < 0) | (df_not_null[col] > 3000)
        df_not_null.loc[invalid, col] = np.nan
        df_not_null = df_not_null.dropna(subset=[col])
        df_not_null[col] = df_not_null[col].astype(int)
    # clean time_increment
    df_not_null = df_not_null.dropna(subset=['time_base', 'time_sec'])
    df_not_null['time_base'] = df_not_null['time_base'].astype(int)
    df_not_null['time_sec'] = df_not_null['time_sec'].astype(int)
    logging.info("Deleted Row that contain on null in time_base and time_sec")

    # remove rows that not contain black and white id
    df_not_null = df_not_null.dropna(subset=['white_id', 'black_id'])
    logging.info("Deleted Row that contain on null in white_id and black_id")

    # remove duplicated rows
    df_not_null = df_not_null.drop_duplicates()
    logging.info("Remove Duplicated")
    print("step 6: repair invalid value is finished for chess:-")
    return df_not_null

# step 6: Dealing With invalid value in players
def dealing_with_invalid_value_players(df_not_null):
    print("step 6: repair invalid value is started for players:-")
    # remove duplicated rows
    df_not_null = df_not_null.drop_duplicates()
    # remove rows that not contain username
    df_not_null = df_not_null.dropna(subset=['username'])
    logging.info("remove rows that contain on missing (null) username ")
    print("step 6: repair invalid value is Finished Player for chess:-")
    return df_not_null

# step 7: Validation chess
def validate_chess(df_treated):
    print("validation Started For chess")
    assert df_treated['black_id'].notna().all(), "black_id column contains null values"
    assert df_treated['white_id'].notna().all(), "white_id column contains null values"
    assert df_treated['rated'].notna().all(), "rating column contains null values"

    print("validation Finished For chess")
    return df_treated

# step 7: Validation players
def validate_players(df_treated):
    print("validation Started For Player")
    # validate username
    assert df_treated['username'].notna().all(), "username column contains null values"
    assert df_treated['username'].isna().sum() == 0, "Found null usernames"
    duplicate_usernames = df_treated['username'].duplicated().sum()
    assert duplicate_usernames == 0, f"{duplicate_usernames} duplicate usernames"

    # valid status
    valid_status = ['active', 'inactive', 'unknown']
    invalid_status = df_treated[~df_treated['account_status'].isin(valid_status)]
    assert len(invalid_status) == 0, "rows contain invalid status"

    print("validation Finished For Player")
    return df_treated