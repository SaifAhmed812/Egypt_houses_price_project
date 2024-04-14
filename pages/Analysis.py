import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.io as pio
from   plotly.subplots import make_subplots

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
#-----------------------------------------------------------------------------------

st.markdown("<h1 style='text-align: center; color: white;'>Choose a category</h1>", unsafe_allow_html=True)
value = st.selectbox("",["Distribution according to the city","Price of homes","Delivery date","Payment options"])

if value == "Distribution according to the city":
    #============================================================ Units avalability according to the location

    st.markdown("<h1 style='text-align: center; color: white;'>Units avalability according to the location</h1>", unsafe_allow_html=True)
    st.plotly_chart(px.histogram(df, y ="City",color_discrete_sequence = px.colors.qualitative.Dark2,nbins = 100))

    #============================================================ Top 9 Cites

    st.markdown("<h1 style='text-align: center; color: white;'>Top 9 Cites</h1>", unsafe_allow_html=True)
    top_count_cities = df.City.value_counts().head(9).reset_index()
    top_count_cities.columns = ["City","Count"]
    st.plotly_chart(px.pie(data_frame= top_count_cities,names="City",values = "Count",hole =0.4))


elif value == "Price of homes":

    tab1,tab2,tab3 = st.tabs(["Location","Area and floor level","Type of home"])
    
    with tab1 :
        #=========================================== Prices versus city

        st.markdown("<h1 style='text-align: center; color: white;'>Prices versus city</h1>", unsafe_allow_html=True)
        top_Price_cities = pd.DataFrame(data = df.groupby("City").Price.mean().sort_values(ascending = False).head(9))
        top_Price_cities = top_Price_cities.rename(columns = {"City":"City","City":"Price"})
        top_Price_cities = top_Price_cities.reset_index()


        st.plotly_chart(px.histogram(top_Price_cities , x = "City",y="Price"
             ,color_discrete_sequence =px.colors.qualitative.D3
             ,marginal = "box"))
        st.table(top_Price_cities)

        #=========================================== barplot
        
        df.groupby("City")["Price"].mean()
        fig, ax = plt.subplots()
        sns.barplot(data = top_Price_cities , x = "City",y="Price",palette = "icefire", ax= ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)       

        #=========================================== pie chart

        st.plotly_chart(px.pie(data_frame=top_Price_cities,names="City",values="Price"))

        #===========================================

        col1 ,col2,col3 = st.columns(3)
        with col1:
            st.metric(label ="Gouna" ,value = "9M",delta = "19.8%")
        with col2:
            st.metric(label ="Glim" ,value = "5M",delta = "11.3%")  
        with col3:
            st.metric(label ="North Coast" ,value = "5M",delta = "10.9%")
            


    with tab2 :

        area_price = df[df["City"] == "North Coast"][["Area","Price","Level"]]
        fig, ax = plt.subplots()
        sns.stripplot(x="Area",y="Price",data=area_price ,ax =ax)
        st.pyplot(fig)

        #============================================
        def area_range(x):
            if (x >= 100.0) & (x<= 160.0):
                return "100 to 160 m²"
            elif (x > 160.0) & (x <= 200.0):
                return "160 to 200 m²"
            elif (x > 200.0) & (x <= 250.0):
                return "200 to 250 m²"
            elif (x > 250.0) & (x <= 400.0):
                return "250 to 400 m²"

        price_area = df[["Price","Area"]].reset_index()
        price_area["Average Price"] = price_area["Price"]
        price_area["Area"] = price_area["Area"].apply(area_range)
        price_area1 = price_area.groupby("Area")["Average Price"].mean().round(5).reset_index()

        st.plotly_chart(px.bar(data_frame=price_area1,x="Area" , y = "Average Price",color_discrete_sequence=px.colors.qualitative.Dark2 ))

        #==========================================
        col1 ,col2,col3,col4 = st.columns(4)
        with col1:
            st.metric(label ="100 to 160 m²" ,value = "2.5M")
        with col2:
            st.metric(label ="160 to 200 m²" ,value = "3.3M")  
        with col3:
            st.metric(label ="200 to 250 m²" ,value = "4.6M")
        with col4:
            st.metric(label ="250 to 400 m²" ,value = "7M")
        
        #======================================
        
        fig = px.line(price_area1,x='Area',y='Average Price',text='Average Price',hover_name='Area',markers=True,template='plotly_dark')
        st.plotly_chart(fig)
            
        #======================================
        st.title("Floor and Prices")
        price_floor = df.groupby('Level').Price.mean().reset_index(name='Price')
        price_floor.sort_values("Level",ascending =True)

        fig, ax = plt.subplots()
        sns.barplot(data=price_floor,x="Level",y="Price")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    with tab3 :
        #============================================ Bar chart

        st.markdown("<h1 style='text-align: center; color: white;'>Units price available according to Type</h1>", unsafe_allow_html=True)

        types = df.groupby("Type")["Price"].mean().sort_values(ascending =True).reset_index(name='Price')
        st.plotly_chart(px.bar(x="Price",y="Type",data_frame=types,color_discrete_sequence=px.colors.sequential.Magenta))
        
        #============================================ pie chart
        
        st.plotly_chart(px.pie(data_frame=types,names="Type",values="Price"))

        
   

elif value == "Delivery date":
    #=========================================== pie chart
        st.markdown("<h1 style='text-align: center; color: #2E91E5;'>Units</h1>", unsafe_allow_html=True)

        Delivery_Term = df.groupby("Delivery_Term").size().sort_values(ascending =True).reset_index(name='counts')
        st.plotly_chart(px.pie(data_frame = Delivery_Term ,names= "Delivery_Term",values ="counts",color_discrete_sequence = px.colors.sequential.GnBu_r))
    
    #=========================================== Bar chart

        Delivery_Term = df.groupby(['Delivery_Term',"Type"]).size().sort_values(ascending =True).reset_index(name='counts')
        st.plotly_chart(px.bar(x="counts",y="Delivery_Term",data_frame=Delivery_Term, color = "Type",
        color_discrete_sequence=px.colors.qualitative.Bold))

    #============================================ Bar chart
        
        Delivery_Date = df.groupby(['Delivery_Date',"Type"]).size().sort_values(ascending =True).reset_index(name='counts')
        Delivery_Date = Delivery_Date.convert_dtypes()
        

    #============================================ Date of Receiving the units
        st.markdown("<h1 style='text-align: center; color: #00A08B;'>Date of Receiving the units</h1>", unsafe_allow_html=True)

        st.table(Delivery_Date.head(6))

        fig = px.bar(x="counts",y="Delivery_Date",data_frame=Delivery_Date,color = "Type",
       color_discrete_sequence=['#ff9999','#66b3ff','#AF0038','#ffcc99',"#00A08B","yellow","#cea9bc","#0a417a","#A777F1","#005F60"])
        fig.update_layout(height=500)
        st.plotly_chart(fig)

    #============================================
    
    
        Delivery_Date.groupby("Delivery_Date")["counts"].sum()
        Date_of_Receiving_the_units = pd.DataFrame(data = 
                                            {"Ready to receive":3442,
                                                "Soon":508,
                                                "by 2022":51,
                                                "by 2023":238,
                                                "by 2024":337,
                                                "by 2025":302,
                                                "by 2026":147,
                                                "by 2027":3,
                                                "within 6 months" :53
                                            },index=[0])
        
        st.dataframe(Date_of_Receiving_the_units)
    

elif value == "Payment options":
    #================================= Payment methods
    
    st.markdown("<h1 style='text-align: center; color: white;'>Payment methods</h1>", unsafe_allow_html=True)
    
    index = pd.DataFrame(data = df[df["Payment_Option"] != "Unknown Payment"])["Payment_Option"].reset_index()
    fig, ax = plt.subplots()
    sns.countplot(x="Payment_Option",data=index,palette="icefire")
    st.pyplot(fig)

    #================================= pie chart
    indexpie= index["Payment_Option"].value_counts().reset_index()
    indexpie.reset_index()
    indexpie[["Payment_Option","count"]] = indexpie[["index","Payment_Option"]]

    st.plotly_chart(px.pie(data_frame=indexpie,names="Payment_Option",values="count"))


        










