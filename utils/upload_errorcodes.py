import streamlit as st
import pandas as pd 
from datetime import datetime
from connection import get_update_connection


error_col_list = [
    "DateRange",
    "Bank",
    "Type",
    "count",
    "error"
]

def update_error_sheet(existing_data, new_data):
    try:
        # Iterate through new data
        for _, new_row in new_data.iterrows():
            date, bank, error , type = new_row['DateRange'], new_row['Bank'], new_row['error'] , new_row['Type']
            
            # Check if the date, bank, and error combination already exists
            match = existing_data[(existing_data['DateRange'] == date) & 
                                (existing_data['Bank'] == bank) & 
                                (existing_data['error'] == error) & (existing_data['Type'] == type)]
            if not match.empty:
                # Update the 'count' for the existing row
                existing_data.loc[match.index, 'count'] = new_row['count']
            else:
                # Append new row
                existing_data = existing_data.append(new_row, ignore_index=True)
        
        return existing_data
    except:
        print("Something went wrong")


def upload_error_csv(data , bank , type , start_date , end_date):
    
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
    columns_to_keep_actual = [col for col in error_col_list if col in data.columns]
    filtered_data = data[columns_to_keep_actual]
    
    filtered_data['error'] = filtered_data['error'].astype(str)
    
    conn = get_update_connection()
    client_data = conn.read(worksheet="ErrorCodes")
    client_data.dropna(how='all', inplace=True)

    filtered_data = filtered_data.groupby('error').agg({
                        'DateRange': 'first',    # Keep the first date for each group
                        'Bank': 'first',    # Keep the first bank for each group
                        'Type': 'first',    # Keep the first bank for each group
                        'count': 'sum'      # Sum the counts for each group
                    }).reset_index()
    
    updated_data = update_error_sheet(client_data, filtered_data)
    cre = conn.update(worksheet="ErrorCodes" , data=updated_data)
