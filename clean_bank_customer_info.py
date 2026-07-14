import logging
import pandas as pd
import numpy as np

# Configure production logging framework instead of raw print statements
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_bank_churn_data(file_path: str) -> pd.DataFrame:
    #"""
    #Executes a vectorized data-cleaning pipeline for banking churn analysis.
    #Addresses structural column drops, text anomalies, and risk-adjusted imputations.
   #"""
    logging.info(f"Initiating pipeline. Ingesting raw data from: {file_path}")
    df = pd.read_csv(file_path)
    
    # 1. STRUCTURAL CLEANUP: Remove unaligned system artifacts & duplicate profiles
    unnamed_cols = [col for col in df.columns if col.startswith('Unnamed:')]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)
        
    df.drop_duplicates(subset=['CustomerId'], keep='first', inplace=True)
    
    # 2. CATEGORICAL STANDARDIZATION: Resolve geographical data-entry anomalies
    geo_normalization = {'FRA': 'France', 'French': 'France'}
    df['Geography'] = df['Geography'].replace(geo_normalization)
    df['Surname'] = df['Surname'].fillna('Unknown')
    
    # 3. NUMERICAL IMPUTATION: Handle missing demographic fields via column mean
    mean_age = df['Age'].mean()
    df['Age'] = df['Age'].fillna(mean_age)
    
    # 4. RISK-ADJUSTED TRANSFORMATION: Vectorized optimization for monetary metrics
    # Strips currency icons, neutralizes corrupt codes (-999999), and converts once to float
    df['EstimatedSalary'] = (
        df['EstimatedSalary']
        .astype(str)
        .str.replace('€', '', regex=False)
        .str.replace(r'-\s*999999', 'NaN', regex=True)
    )
    df['EstimatedSalary'] = pd.to_numeric(df['EstimatedSalary'], errors='coerce')
    
    # Contextual Imputation: Segment peer group by risk threshold to calculate median
    credit_peer_mask = df['CreditScore'] >= 500
    peer_median_salary = df[credit_peer_mask]['EstimatedSalary'].median()
    
    df['EstimatedSalary'] = df['EstimatedSalary'].fillna(peer_median_salary)
    
    # 5. DATA TYPE ENFORCEMENT
    df['Age'] = df['Age'].astype(int)
    
    logging.info(f"Pipeline executed successfully. Clean dataset integrity profile: {df.shape}")
    return df

if __name__ == "__main__":
    SOURCE_PATH = '/Users/rohinisaichandramunnangi/Downloads/Bank_Customer_Churn/Bank_Churn_Customer_info_Raw.csv'
    clean_df = clean_bank_churn_data(SOURCE_PATH)