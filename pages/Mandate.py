import streamlit as st
import pandas as pd
from connection import get_connection
import plotly.express as px

from sidebar import create_sidebar

st.set_page_config(layout="wide")

create_sidebar()
# Create a connection object.
conn = get_connection()
df = conn.read(worksheet="Volume")
df.dropna(how='all' , inplace=True)

df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y' , errors='coerce')
cols_to_convert = [col for col in df.columns if col not in ['Bank', 'Date']]

st.title("Mandate Analytics")

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

with st.expander("Mandate Creation"):

    # st.subheader("Mandate Creation")

    cre_df = pd.DataFrame(filtered_df)
    cre_df['Date'] = pd.to_datetime(cre_df['Date'], format='%d/%m/%Y')



    cre_df["Mandate creation sr"] = (cre_df["Mandate creation succvol"] * 100) / cre_df["Mandate creation Vol"]

    # Create the line chart
    cre_sr_fig = px.line(cre_df,
                x='Date', 
                y='Mandate creation sr', 
                color='Bank', 
                title='Mandate Creation sr ' , 
                markers=True,
                labels={"Mandate creation sr": "Percentage (%)" , "Date" : "Date"},
                text=["{:.1f} %".format(value) for value in cre_df["Mandate creation sr"]])

    # cre_sr_fig.update_yaxes(tick0=0, dtick=1000)

    cre_sr_fig.update_traces(textposition="bottom center")

    cre_sr_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
    # Streamlit app
    st.plotly_chart(cre_sr_fig)

    # Create the line chart
    cre_vol_fig = px.line(cre_df,
                x='Date', 
                y='Mandate creation Vol', 
                color='Bank', 
                title='Mandate Creation Volume ' , 
                markers=True,
                labels={"Mandate creation Vol": "Volume (M)" , "Date" : "Date"},
                text=["{:.1f} k".format(value/1000) for value in cre_df["Mandate creation Vol"]])

    cre_vol_fig.update_yaxes(tick0=0, dtick=1000)

    cre_vol_fig.update_traces(textposition="bottom center")

    cre_vol_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
    # Streamlit app
    st.plotly_chart(cre_vol_fig)

    # Create the line chart
    cre_succ_vol_fig = px.line(cre_df,
                x='Date', 
                y='Mandate creation succvol', 
                color='Bank', 
                title='Mandate creation succvol' , 
                markers=True,
                labels={"Mandate creation succvol": "Volume (M)" , "Date" : "Date"},
                text=["{:.1f} k".format(value/1000) for value in cre_df["Mandate creation succvol"]])

    cre_succ_vol_fig.update_yaxes(tick0=0, dtick=1000)

    cre_succ_vol_fig.update_traces(textposition="bottom center")

    cre_succ_vol_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
    # Streamlit app
    st.plotly_chart(cre_succ_vol_fig)

with st.expander("Mandate Excution"):

    # st.subheader("Mandate Creation")

    exe_df = pd.DataFrame(filtered_df)
    exe_df['Date'] = pd.to_datetime(exe_df['Date'], format='%d/%m/%Y')



    exe_df["Mandate Execution sr"] = (exe_df["Mandate SuccVolume Execution"] * 100) / exe_df["Mandate Volume Execution"]

    # Create the line chart
    exe_sr_fig = px.line(exe_df,
                x='Date', 
                y='Mandate Execution sr', 
                color='Bank', 
                title='Mandate Execution sr ' , 
                markers=True,
                labels={"Mandate Execution sr": "Percentage (%)" , "Date" : "Date"},
                text=["{:.1f} %".format(value) for value in exe_df["Mandate Execution sr"]])

    # cre_sr_fig.update_yaxes(tick0=0, dtick=1000)

    exe_sr_fig.update_traces(textposition="bottom center")

    exe_sr_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
    # Streamlit app
    st.plotly_chart(exe_sr_fig)

    # Create the line chart
    exe_vol_fig = px.line(exe_df,
                x='Date', 
                y='Mandate Volume Execution', 
                color='Bank', 
                title='Mandate Volume Execution' , 
                markers=True,
                labels={"Mandate Volume Execution": "Volume (M)" , "Date" : "Date"},
                text=["{:.1f} k".format(value/1000) for value in exe_df["Mandate Volume Execution"]])

    exe_vol_fig.update_yaxes(tick0=0, dtick=10000)

    exe_vol_fig.update_traces(textposition="bottom center")

    exe_vol_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
    # Streamlit app
    st.plotly_chart(exe_vol_fig)

    # Create the line chart
    exe_succ_vol_fig = px.line(exe_df,
                x='Date', 
                y='Mandate SuccVolume Execution', 
                color='Bank', 
                title='Mandate SuccVolume Execution' , 
                markers=True,
                labels={"Mandate SuccVolume Execution": "Volume (M)" , "Date" : "Date"},
                text=["{:.1f} k".format(value/1000) for value in exe_df["Mandate SuccVolume Execution"]])

    exe_succ_vol_fig.update_yaxes(tick0=0, dtick=10000)

    exe_succ_vol_fig.update_traces(textposition="bottom center")

    exe_succ_vol_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
    # Streamlit app
    st.plotly_chart(exe_succ_vol_fig)

