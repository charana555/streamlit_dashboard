import streamlit as st
import pandas as pd
from connection import get_connection
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout="wide")

# Create a connection object.
conn = get_connection()
df = conn.read(worksheet="Volume")
df.dropna(how='all' , inplace=True)

df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y' , errors='coerce')
cols_to_convert = [col for col in df.columns if col not in ['Bank', 'Date']]

st.title("Credit Card Analytics")

cols = st.columns(4)

available_dates = df["Date"].unique()

max_date = pd.to_datetime(available_dates , format='%d/%m/%Y').max()
acc_min_date = pd.to_datetime(available_dates , format='%d/%m/%Y').min()
min_date = max_date - pd.Timedelta(days=13)

with cols[0]:
    start_date = st.date_input("Start Date", min_value=acc_min_date, max_value=max_date, value=min_date)
with cols[1]:    
    end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)


filtered_df = df.query('Date >= @start_date and Date <= @end_date')


filtered_df = filtered_df.sort_values(by='Date')

st.markdown("######")

df = pd.DataFrame(filtered_df)
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

df["Credit Card sr"] = (df["CREDIT CARD Succvolume"] * 100) / df["CREDIT CARD Volume"]

# Create the line chart
cre_sr_fig = px.line(df,
            x='Date', 
            y='Credit Card sr', 
            color='Bank', 
            title='Credit Card sr ' , 
            markers=True,
            # barmode='group',
            labels={"Credit Card sr": "Percentage (%)" , "Date" : "Date"},
            text=["{:.1f} %".format(value) for value in df["Credit Card sr"]])

# cre_sr_fig.update_yaxes(tick0=0, dtick=1000)

cre_sr_fig.update_traces(textposition="bottom center")

cre_sr_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
# Streamlit app
st.plotly_chart(cre_sr_fig)

# Create the line chart
cre_vol_fig = px.line(df,
            x='Date', 
            y='CREDIT CARD Volume', 
            color='Bank', 
            title='CREDIT CARD Volumeume ' , 
            markers=True,
            labels={"CREDIT CARD Volume": "Volume (M)" , "Date" : "Date"},
            text=["{:.1f} k".format(value/1000) for value in df["CREDIT CARD Volume"]])

cre_vol_fig.update_yaxes(tick0=0, dtick=1000)

cre_vol_fig.update_traces(textposition="bottom center")

cre_vol_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
# Streamlit app
st.plotly_chart(cre_vol_fig)

# Create the line chart
cre_succ_vol_fig = px.line(df,
            x='Date', 
            y='CREDIT CARD Succvolume', 
            color='Bank', 
            title='CREDIT CARD Succvolume' , 
            markers=True,
            labels={"CREDIT CARD Succvolume": "Volume (M)" , "Date" : "Date"},
            text=["{:.1f} k".format(value/1000) for value in df["CREDIT CARD Succvolume"]])

cre_succ_vol_fig.update_yaxes(tick0=0, dtick=1000)

cre_succ_vol_fig.update_traces(textposition="bottom center")

cre_succ_vol_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
# Streamlit app
st.plotly_chart(cre_succ_vol_fig)
