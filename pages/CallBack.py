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

st.title("CallBack Analytics")

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


# st.subheader("Mandate Creation")

df = pd.DataFrame(filtered_df)
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')



df["CallBack sr"] = (df["CALLBACK Succvolume"] * 100) / df["CALLBACK Volume"]

# Create the line chart
cre_sr_fig = px.bar(df,
            x='Date', 
            y='CallBack sr', 
            color='Bank', 
            title='CallBack sr' , 
            # markers=True,
            barmode='group',
            labels={"CallBack sr": "Percentage (%)" , "Date" : "Date"},
            text=["{:.1f} %".format(value) for value in df["CallBack sr"]]
            )

# cre_sr_fig.update_yaxes(tick0=0, dtick=1000)

# cre_sr_fig.update_traces(textposition="bottom center")

cre_sr_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
# Streamlit app
st.plotly_chart(cre_sr_fig)

# Create the line chart
cre_vol_fig = px.line(df,
            x='Date', 
            y='CALLBACK Volume', 
            color='Bank', 
            title='CALLBACK Volume' , 
            markers=True,
            labels={"CALLBACK Volume": "Volume (M)" , "Date" : "Date"},
            text=["{:.1f} M".format(value/1000000) for value in df["CALLBACK Volume"]])

cre_vol_fig.update_yaxes(tick0=0, dtick=1000000)

cre_vol_fig.update_traces(textposition="bottom center")

cre_vol_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
# Streamlit app
st.plotly_chart(cre_vol_fig)

# Create the line chart
cre_succ_vol_fig = px.line(df,
            x='Date', 
            y='CALLBACK Succvolume', 
            color='Bank', 
            title='CALLBACK Succvolume' , 
            markers=True,
            labels={"CALLBACK Succvolume": "Volume (M)" , "Date" : "Date"},
            text=["{:.1f} M".format(value/1000000) for value in df["CALLBACK Succvolume"]])

cre_succ_vol_fig.update_yaxes(tick0=0, dtick=1000000)

cre_succ_vol_fig.update_traces(textposition="bottom center")

cre_succ_vol_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))
# Streamlit app
st.plotly_chart(cre_succ_vol_fig)
