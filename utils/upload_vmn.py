from connection import get_update_connection
from datetime import datetime
vmn_col_list = [
   "DateRange",	
   "Bank",
   "aggregator",	
   "afterExpiry",	
   "notRecieved",	
   "success",	
   "total",
   "successRate"
]

def update_vmn_sheet(existing_data, data):
    for _, row in data.iterrows():
        date, bank , aggregator = row['DateRange'], row['Bank'] , row['aggregator']
        # Check if the date and bank already exist
        match = existing_data[(existing_data['DateRange'] == date) & (existing_data['Bank'] == bank) & (existing_data['aggregator'] == aggregator)]
        if not match.empty:
            # Update existing row
            for col in data.columns:
                if col != 'DateRange' and col != 'Bank' and col != 'aggregator':
                    existing_data.loc[match.index, col] = row[col]
        else:
            # Append new row
            existing_data = existing_data.append(row, ignore_index=True)
    return existing_data

def upload_vmn_csv(data , bank , start_date , end_date):

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
    
    columns_to_keep_actual = [col for col in vmn_col_list if col in data.columns]
    filtered_data = data[columns_to_keep_actual]
    
    conn = get_update_connection()
    client_data = conn.read(worksheet="VMN")
    client_data.dropna(how='all', inplace=True)

    updated_data = update_vmn_sheet(client_data, filtered_data)
    cre = conn.update(worksheet="VMN" , data=updated_data)