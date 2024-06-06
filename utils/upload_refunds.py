import streamlit as st
import pandas as pd 
from datetime import datetime
from connection import get_update_connection

refund_col_list = [
    "DateRange",
    "Bank",
    "Type",
    "count",
    "status"
]

def update_refund_sheet(existing_data, new_data):
    try:
        # Iterate through new data
        for _, new_row in new_data.iterrows():
            date, bank, status , type = new_row['DateRange'], new_row['Bank'], new_row['status'] , new_row['Type']
            
            # Check if the date, bank, and error combination already exists
            match = existing_data[(existing_data['DateRange'] == date) & 
                                (existing_data['Bank'] == bank) & 
                                (existing_data['status'] == status) & (existing_data['status'] == type)]
            if not match.empty:
                # Update the 'count' for the existing row
                existing_data.loc[match.index, 'count'] = new_row['count']
            else:
                # Append new row
                existing_data = existing_data.append(new_row, ignore_index=True)
        
        return existing_data
    except:
        print("Something went wrong")



def upload_refund_csv(data , bank , type , start_date , end_date):

    date_range = f'{start_date} - {end_date}'
    start_date_str, end_date_str = date_range.split(" - ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    start_date_formatted = start_date.strftime("%d/%m/%Y")
    end_date_formatted = end_date.strftime("%d/%m/%Y")

    # Construct the new date range string
    new_date_range = f"{start_date_formatted} - {end_date_formatted}"   
    
    data["DateRange"] = new_date_range
    data["Bank"] = bank
    data["Type"] = type
    
    if 'Online_volume' in data.columns:
        data = data.rename(columns = {'Online_volume' : 'count' , 'Online_status' : 'status'})
    if 'Offline_volume' in data.columns:
        data = data.rename(columns = {'Offline_volume' : 'count' , 'Offline_status' : 'status'})
    columns_to_keep_actual = [col for col in refund_col_list if col in data.columns]
    filtered_data = data[columns_to_keep_actual]
    
    filtered_data['status'] = filtered_data['status'].astype(str)

    total_count = filtered_data['count'].sum()

    filtered_data['sr'] = (filtered_data['count'] * 100) / total_count

    conn = get_update_connection()
    client_data = conn.read(worksheet="Refunds")
    client_data.dropna(how='all', inplace=True)

    updated_data = update_refund_sheet(client_data, filtered_data)
    cre = conn.update(worksheet="Refunds" , data=updated_data)
