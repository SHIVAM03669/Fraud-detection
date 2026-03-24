import pandas as pd
import numpy as np

def load_data(path):
    return pd.read_csv(path)

def basic_cleaning(df):
    # droping duplicates
    df = df.drop_duplicates()

    #handle missing values(agar hoga toh)
    df = df.dropna()

    return df

def transform_amount(df):
    # yeh function log transform karta hai
    df['Amount'] = np.log1p(df['Amount'])
    return df

def run_cleaning_pipeline(path):
    df = load_data(path)
    df = basic_cleaning(df)
    df = transform_amount(df)
    return df