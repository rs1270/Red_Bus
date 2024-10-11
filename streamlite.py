import streamlit as st
import pandas as pd
import re
st.set_page_config(layout="wide")
# Load the CSV file
df = pd.read_csv('govt_bus_detailsfull.csv')
#Create tabs
tab1, tab2, tab3,tab4,tab5,tab6= st.tabs(["Home",'Route Name','Bus Type' ,"Star", "Price",'Availability'])
filtered_df = pd.DataFrame()
with tab1:
    st.write(df)
with tab2:
    selected_route = st.selectbox("Choose a Route:", df['Route_Name'].unique().tolist())
    filtered_data = df[df['Route_Name'] == selected_route]
    st.write(filtered_data)

with tab3:
    bus_type=st.selectbox("Bus Type:", df['Bus_Type'].unique().tolist())
    filtered_data = df[df['Bus_Type'] == bus_type]
    st.write(filtered_data)
with tab4:
    rating = st.radio("Choose a rating for star:", ['Rating 4- 5', 'Rating 3-4', 'Rating 2-3','Rating 1-2','Rating 0-1'])

    if rating == 'Rating 0-1':
        filtered_df = df[(df.Star_Rating > 0) & (df.Star_Rating <= 1)]
    elif rating == 'Rating 1-2':
        filtered_df = df[(df.Star_Rating > 1) & (df.Star_Rating <= 2)]
    elif rating == 'Rating 2-3':
        filtered_df = df[(df.Star_Rating > 2) & (df.Star_Rating <= 3)]
    elif rating == 'Rating 3-4':
        filtered_df = df[(df.Star_Rating > 3) & (df.Star_Rating <= 4)]
    else:
        filtered_df = df[(df.Star_Rating > 4) & (df.Star_Rating <= 5)]
    st.write(filtered_df)


with tab5:
  

        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df = df.dropna(subset=['Price'])
        Price = st.radio("Choose Price:", ['Passenger Bus', 'Normal Bus', 'Delux Bus'])
        if Price == 'Passenger Bus':
            filtered_df = df[df['Price'] <= 500]
        elif Price == 'Normal Bus':
            filtered_df = df[(df['Price'] > 500) & (df['Price'] <= 1000)]
        else:
            filtered_df = df[df['Price'] > 1000]
        st.write(filtered_df)
with tab6:
    available = st.radio("Choose Price:", ['Availabale', 'Filling Fast'])
    df['Seat_Availability'] = df['Seat_Availability'].apply(lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

    if available == 'Filling Fast':
        filtered_df = df[df['Seat_Availability'] < 5]
    else:
        filtered_df = df[df['Seat_Availability'] > 5]

    st.write(filtered_df)