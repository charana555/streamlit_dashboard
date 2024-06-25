import streamlit as st
import pandas as pd 
from datetime import datetime
from connection import get_update_connection

bind_col_list = [
    "Date",	
    "Bank",	
    "Total",	
    "BoundCount",	
    "activatedCount",	
    "verifiedCount",	
    "verifiedBeforeExpiry",	
    "verifiedAfterExpiry"
]

def preprocess_bind_file(df , selected_bank):

    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y' , errors='coerce').dt.strftime('%d/%m/%Y')
    columns_to_keep_actual = [col for col in bind_col_list if col in df.columns]
    filtered_df = df[columns_to_keep_actual]
    filtered_df['Bank'] = selected_bank
    return filtered_df

def update_bind_sheet(existing_data, data):
    for _, row in data.iterrows():
        date, bank = row['Date'], row['Bank']
        # Check if the date and bank already exist
        match = existing_data[(existing_data['Date'] == date) & (existing_data['Bank'] == bank)]
        if not match.empty:
            # Update existing row
            for col in data.columns:
                if col != 'Date' and col != 'Bank':
                    existing_data.loc[match.index, col] = row[col]
        else:
            # Append new row
            existing_data = existing_data.append(row, ignore_index=True)
    return existing_data

def upload_bind_csv(data , bank ):
    
    data = preprocess_bind_file(data , bank)
    conn = get_update_connection()
    client_data = conn.read(worksheet="BindDevice")
    client_data.dropna(how='all', inplace=True)
    
    client_data['Date'] = pd.to_datetime(client_data['Date'], format='%d/%m/%Y' , errors='coerce').dt.strftime('%d/%m/%Y')

    updated_data = update_bind_sheet(client_data, data)

    updated_data['Date'] = pd.to_datetime(updated_data['Date'], format='%d/%m/%Y' , errors='coerce').dt.strftime('%d/%m/%Y')
    
    cre = conn.update(worksheet="BindDevice" , data=updated_data)