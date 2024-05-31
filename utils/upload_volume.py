import streamlit as st
import pandas as pd 
from datetime import datetime
from connection import get_connection



volume_col_list = [
    "Date", "Bank", "P2M_Pay_Volume", "P2M_COLLECT_Volume", "P2P_Pay_Volume",
    "P2P_COLLECT_Volume", "P2M_Pay_Succvolume", "P2M_Collect_Succvolume",
    "P2P_Pay_Succvolume", "P2P_Collect_Succvolume", "CREDIT CARD Volume",
    "CREDIT CARD Succvolume", "CALLBACK Volume", "CALLBACK Succvolume",
    "UPI LITE Volume", "UPI LITE Succvolume", "Mandate Volume Execution",
    "Mandate SuccVolume Execution", "Mandate creation Vol",
    "Mandate creation succvol", "CC ONUS Vol", "CC OFFUS VOL",
    "CC ONUS sUCC-Vol", "CC OFFUS Succ-VOL"
]

def preprocess_srvol_file(df , selected_bank):
    if "day" in df.columns:
        df = df.rename(columns={'day': 'Date'})
    
    columns_to_keep_actual = [col for col in volume_col_list if col in df.columns]
    filtered_df = df[columns_to_keep_actual]
    filtered_df['Bank'] = selected_bank
    return filtered_df

def preprocess_cctxn_file(df , selected_bank):
    if "date" in df.columns:
        df = df.rename(columns={'date': 'Date' , 'successVolume' : 'CREDIT CARD Succvolume' , 'totalVolume' : 'CREDIT CARD Volume'})
    df['Date'] = pd.to_datetime(df['Date'] + f'/{datetime.now().year}', format='%m/%d/%Y').dt.strftime('%d/%m/%Y')
    columns_to_keep_actual = [col for col in volume_col_list if col in df.columns]
    filtered_df = df[columns_to_keep_actual]
    filtered_df['Bank'] = selected_bank    
    return filtered_df

def update_sheet(existing_data, data):
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


def upload_csv(data , bank , type):
    
    if type == 'SR_Vol':
        data = preprocess_srvol_file(data , bank)
    elif type == 'CC_TXN':
        data = preprocess_cctxn_file(data , bank)    
    
    conn = get_connection()
    client_data = conn.read(worksheet="Volume")
    client_data.dropna(how='all', inplace=True)
    
    
    updated_data = update_sheet(client_data, data)
    
    cre = conn.update(worksheet="Volume" , data=updated_data)
