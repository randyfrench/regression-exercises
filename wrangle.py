#import libraries
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Connection
from env import host, user, password

# Acquire Zillow Data

# Create function to get the necessary connection url.
def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db. It takes in a string 
    name of a database as an argument
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


#create function to retrieve zillow data
def new_zillow_data():
    '''
    This function reads the Telco data from the Codeup db
    and returns a pandas DataFrame with three joined tables and all columns.
    '''
    
    sql_query = '''
    SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount,fips
    FROM properties_2017
    WHERE propertylandusetypeid = 261 
    '''
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    return df

def get_zillow_data():
    '''
    This function reads in zillow data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('zillow_df.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('zillow_df.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_zillow_data()
        
        # Cache data
        df.to_csv('zillow_df.csv')
        
    return df

def handle_NaN():
    '''
    This function handles the NaN values for the Zillow data (could be used for other dataframes). 
    Takes in a dataframe and returns a dataframe with the NaN values replaced with the mean.
    '''

    # replaces NaN with the mean of the column
    imputer = SimpleImputer(strategy = 'mean')
    for col in df.columns:
        df[[col]] = imputer.fit_transform(df[[col]])

    return df

def wrangle_zillow():
    '''
    This function handels getting the data from the zillow database and getting it ready to visualize.
    It returns the dataframe ready to work with.
    Uses other helper functions in wrangle.py to get this done. 
    '''

    df = get_zillow_data()

    df = handle_NaN()

    return df