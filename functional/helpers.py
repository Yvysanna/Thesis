import pandas as pd
import re

def get_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    '''Loads the data from the excel files'''
    full_male = pd.read_csv('data/male_complete.csv')
    full_female = pd.read_csv('data/female_complete.csv')

    return full_male, full_female

def process(df: pd.DataFrame) -> pd.DataFrame:
    '''Returns a filtered version of the df containing only data we have for every row'''
    return df[['day', 'time', 'hub name','playlist name', 'type']]

def add_counts(df: pd.DataFrame) -> pd.DataFrame:
    df['playlist count'] = df.groupby('playlist name')['playlist name'].transform('count')
    df['hub count'] = df.groupby('hub name')['hub name'].transform('count')
    return df

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
    # df['time'] = df.time.astype(str).apply(lambda x: int(x[:2]))

    # for i, time in df.time.iteritems():
    #     if time < 12:
    #         df.iloc[i] = 'morning'
    #     elif time >=12<19:
    #         df.iloc[i] = 'afternoon'
    #     else:
    #         df.iloc[i] = 'evening'
    return df

def map_color(x, all) -> list[str]:
    '''Creates colorlist for male and female user's features'''
    return ['blue' if e in x else 'red' for e in all]