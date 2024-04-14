import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.io as pio
from   plotly.subplots import make_subplots

#st.metric(label ="wind speed" ,value = "120 m\s",delta = "-140 m\s")
df = pd.read_csv("Egypt_Houses_Price.csv")

# Cleaning data

df.replace("Unknown", np.nan , inplace =True)
df.replace("Unknown ", np.nan , inplace =True)

df.dropna(inplace = True)
df = df.convert_dtypes()

df["Price"] = df.Price.astype("int32")
df["Bedrooms"] = df.Bedrooms.astype("float32")
df["Bathrooms"] = df.Bathrooms.astype("float32")
df["Area"] = df.Area.astype("float32")

df = df.reset_index()
df.drop("index" ,inplace =True ,axis =1)

index = df[df.City == "(View phone number)"].index
df.drop(index,axis =0 ,inplace =True)

#==========================================================

st.markdown("<h1 style='text-align: center; color: white;'>Houses in Egpyt</h1>", unsafe_allow_html=True)
st.image("https://a0.muscache.com/im/pictures/miso/Hosting-580507541081241789/original/5908727a-7213-4e4d-a466-28950ef9baca.jpeg?im_w=1200")

if st.checkbox("Show Dataframe"):
    st.table(df.head(7))

st.write("## Discription")
st.dataframe(df.describe())