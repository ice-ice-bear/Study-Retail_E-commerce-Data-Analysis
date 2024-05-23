
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Load the data
@st.cache_data
def load_data():
    Olist = pd.read_csv("C:/Users/pc/Documents/GitHub/Study-Retail_E-commerce-Data-Analysis/List_of_Orders.csv")
    Detail = pd.read_csv("C:/Users/pc/Documents/GitHub/Study-Retail_E-commerce-Data-Analysis/Order_Details.csv")
    data = Olist.merge(Detail, on="Order ID")

    return data

# Data Preprcessing
def preproc():
    data['Order Date'] = pd.to_datetime(data['Order Date'], format = '%d-%m-%Y')
    data['year'] = data['Order Date'].dt.year
    data['month'] = data['Order Date'].dt.month
    data['yearmonth'] = data['Order Date'].dt.strftime('%Y-%m')
    #data['yearmonth'] = data['Order Date'].astype('str').slice(0,7)

    return data   

# line chart
def line_chart(data, x, y, title):
    df = data.groupby(x).agg({y: 'sum'}).reset_index()
    fig = px.line(df, x=x, y=y, title=title)
    fig.show()

    return df, fig

# bar chart
def bar_chart(data, x, y, color=None):
  if color is not None:
    index = [x, color]  # Assign a list to index if color is provided
  else:
    index = x  # Assign x to index if color is None

  df = data.pivot_table(index=index, values=y, aggfunc='sum').reset_index()
  fig = px.bar(df, x=x, y=y, color=color)
  fig.show()

  return fig

def heat_map(data, z, title):
    df = data.pivot_table(index = ['State', 'Sub-Category'], values = [z], aggfunc='sum').reset_index()
    fig = px.density_heatmap(df, x = 'State', y = 'Sub-Category', z = z, title = title)
    fig.show()

    return fig

if __name__ == "__main__":
  st.title('E-Commerce Data Analyis')
  st.write('Make Visual DashBoard')

  #load data
  data = load_data()
  #data preprocess
  data = preproc()


st.subheader('Analyze Monthly Sales')
with st.form('form', clear_on_submit =True):
  col1, col2 = st.columns(2)
  submitted1 = col1.form_submit_button('Sales Quantity Table')
  submitted2 = col2.form_submit_button('Sales Amount Table')

  if submitted1:
    df1, fig1 = line_chart(data, 'yearmonth', 'Quantity', 'Sales Quantity by Month')
    st.dataframe(df1, T)
    st.plotly_chart(fig1, theme = 'streamlit', use_container_width = True)
  elif submitted2:
    df2, fig2 = line_chart(data, 'yearmonth', 'Amount', 'Sales by Month')
    st.dataframe(df2, T)
    st.plotly_chart(fig2, theme = 'streamlit', use_container_width = True)

st.subheader('Analyze Sales by Product')
col1, col2 = st.columns(2)
with col1:
  col1.subheader("Sales through Category")
  fig3 = bar_chart(data, 'Category', 'Quantity')
  st.plotly_chart(fig3, theme = 'streamlit', use_container_width = True)

with col2:
  col2.subheader("Monthly Sales Quantity by State")
  fig4 = bar_chart(data, 'yearmonth', 'Quantity', 'Category')
  st.plotly_chart(fig4, theme = 'streamlit', use_container_width = True)

st.subheader('Major Product through local')
tab1, tab2 = st.tabs(['Quantity heat map', 'Amount heat map'])
with tab1:
  fig5 = heat_map(data, 'Quantity', 'Quantity heat map')
  st.plotly_chart(fig5, theme = 'streamlit', use_container_width = True)
with tab2:
  fig6 = heat_map(data, 'Amount', 'Amount heat map')
  st.plotly_chart(fig6, theme = 'streamlit', use_container_width = True)
