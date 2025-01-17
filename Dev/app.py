import pandas as pd
import requests
from datetime import datetime
import os

#----------- Function to fetch JSON data ----------------
def Json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = [response.json()]
    except Exception as e:
        print(f"Error occurred: {e}")
        json_data = [] 

    return json_data

#-------------- Function to flatten the Json Data --------------
def flatten(df): 
    while True:
        # Identify columns with lists or dictionaries
        nested_columns = [
            col for col in df.columns
                if any(isinstance(i, (dict, list)) for i in df[col])
        ]
 
        if not nested_columns:
            break # Exit loop if no nested columns remain

        for col in nested_columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():
            # Explode lists into multiple rows
                df = df.explode(col).reset_index(drop=True)

            elif df[col].apply(lambda x: isinstance(x, dict)).any():
            # Expand dictionaries into new columns
                expanded = pd.json_normalize(df[col])
                expanded.columns = [f"{col}_{subcol}" for subcol in expanded.columns]
                df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
 
        return df

#----------------- Function to transform the dataframe -------------------
def transformation(df):
    new_order = [
    "id", "username", "first_name", "last_name", "gender", 
    "phone_number", "address_country", "subscription_plan", 
    "subscription_status", "subscription_payment_method"
    ]

    df = df[new_order]
    df = df.copy()
    df.rename(columns = {"address_country" : "Country"} , inplace = True)
    return df

#---------------- Function to write the data to a specific location ---------------------
def write_file(write_folder, df):
 
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    file_name = f"output_{timestamp}.csv"
    write_path = os.path.join(write_folder, file_name)

    if not os.path.exists(write_folder):
        os.makedirs(write_folder)
        print(f"Directory {write_folder} created.")

    df.to_csv(write_path, index=False)
    print(f"File is written to {write_path}")

#---------------- Main code -----------------------------
url = "https://random-data-api.com/api/v2/users"

raw_data = Json_data(url)
df = pd.DataFrame(raw_data)

df = flatten(df)
df = transformation(df)

write_path = r"E:\mini project\Output"
write_file(write_path , df)
