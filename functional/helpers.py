import pandas as pd
import re

def get_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    '''Loads the data from the excel files'''
    full_male = pd.read_excel('data/male_complete.xlsx')
    full_female = pd.read_excel('data/female_complete.xlsx')

    return full_male, full_female

def process(df: pd.DataFrame) -> pd.DataFrame:
    '''Returns a filtered version of the df containing only data we have for every row'''
    return df[['day', 'time', 'hub name','playlist name', 'type']]

def unified(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([df1, df2])

def clean(string: str) -> str:
    '''Cleans texts for semantic comparison'''
    string = str(string).lower().strip()

    # Remove any characters that are not alpha numerical or white spaces or equal sign (because of Ed Sheeran album)
    string = re.sub(r'[^a-z\s\=A-Z0-9]', '', string)
    return string

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    '''Cleans texts for semantic comparison'''
    df['hub name'] = df['hub name'].apply(clean)
    df['playlist name'] = df['playlist name'].apply(clean)

    return df