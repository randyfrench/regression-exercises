import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

# Telco Prep

def prep_telco_data(df):
    
    '''
    This function handles nulls, duplicates, strings, encoding_columns and then return the df
    '''
    # drop any duplicates
    df.drop_duplicates(inplace=True)
    
    # fill any empty spaces with np.nan
    df.replace(' ', np.nan, inplace=True)
    
    # drop rows that contain null values, they are a small percentage
    df.dropna(axis=0, inplace=True)
    
    # convert total_charges to a numeric data type
    df = df.astype({'total_charges': 'float64'})

    # No computations will be done on 'customer_id' that column will become the index.
    df.set_index('customer_id', drop=True, inplace=True)
    
    # Encode columns that need encoding
    df.gender = df.gender.replace({'Male': 1, 'Female': 0})
    df.partner = df.partner.replace({'Yes': 1, 'No': 0})
    df.dependents = df.dependents.replace({'Yes': 1, 'No': 0})
    df.phone_service = df.phone_service.replace({'Yes': 1, 'No': 0})
    df.multiple_lines = df.multiple_lines.replace({'No phone service': 0, 'Yes': 1, 'No': 0})
    df.online_security = df.online_security.replace({'No internet service': 0, 'Yes': 1, 'No': 0})
    df.online_backup = df.online_backup.replace({'No internet service': 0, 'Yes': 1, 'No': 0})
    df.device_protection = df.device_protection.replace({'No internet service': 0, 'Yes': 1, 'No': 0})
    df.tech_support = df.tech_support.replace({'No internet service': 0, 'Yes': 1, 'No': 0})
    df.streaming_tv = df.streaming_tv.replace({'No internet service': 0, 'Yes': 1, 'No': 0}) 
    df.streaming_movies = df.streaming_movies.replace({'No internet service': 0, 'Yes': 1, 'No': 0})
    df.paperless_billing = df.paperless_billing.replace({'Yes': 1, 'No': 0})
    df.churn = df.churn.replace({'Yes': 1, 'No': 0})
    df.contract_type = df.contract_type.replace({'Month-to-month': 0, 'One year': 1, 'Two year': 2})
    df.payment_type = df.payment_type.replace({'Mailed check': 0, 'Credit card (automatic)': 1, 'Bank transfer (automatic)': 1,  'Electronic check': 0})
   
    
    # Combine simliar columns and drop the individual ones
    df['online_services'] = df.online_security + df.online_backup
    df = df.drop(columns = ['online_security', 'online_backup'])
    df['streaming_services'] = df.streaming_tv + df.streaming_movies
    df = df.drop(columns=['streaming_tv', 'streaming_movies'])
    
    return(df)



def telco_split(df):
    '''
    This function takes in the telco data acquired by get_telco_data,
    performs a split and stratifies churn column.
    Returns train, validate, and test dataframes.
     '''
    train_validate, test = train_test_split(df, test_size=.2, 
                                           random_state=123, 
                                          stratify=df.churn)
    train, validate = train_test_split(train_validate, test_size=.3, 
                                       random_state=123, 
                                       stratify=train_validate.churn)
    return train, validate, test