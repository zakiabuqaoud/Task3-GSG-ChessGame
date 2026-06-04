import pandas as pd
from pandas import DataFrame
import re
import columns_with_target_types

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

    print("After Removed Null:-")
    print(df_typed.isnull().sum())
    print("step 5: Dealing and treat null : Finished")
    return df_typed


