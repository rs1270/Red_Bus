import streamlit as st
import pandas as pd
import re


st.set_page_config(layout="wide")


# Apply the styling

# Load the CSV file
df = pd.read_csv('govt_bus_detailsfull.csv')
#Create tabs
tab1, tab2= st.tabs(["Home",'Route Name'])
filtered_df = pd.DataFrame()
with tab1:
    st.write(df)

with tab2:
    selected_route = st.selectbox("Choose a Route:", ['Select Route'] + df['Route_Name'].unique().tolist())

if selected_route != 'Select Route':
    filtered_data = df[df['Route_Name'] == selected_route]
    st.write(filtered_data)
    bus_type = st.selectbox("Bus Type:", ['Select Bus Type'] + filtered_data['Bus_Type'].unique().tolist())
    if bus_type != 'Select Bus Type':
        valid_bus_types = filtered_data['Bus_Type'].unique().tolist()
        if bus_type in valid_bus_types:
            filtered_data_bus = filtered_data[filtered_data['Bus_Type'] == bus_type]
            st.write(filtered_data_bus)
        else:
            st.write("Please select a valid bus type.")
   
    rating_range = st.slider("Select a rating range:", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.5)

    if st.button("Apply Filter"):
        filtered_df_star = filtered_data[(filtered_data.Star_Rating >= rating_range[0]) & (filtered_data.Star_Rating <= rating_range[1])]
        st.write("Filtered data based on rating range:", filtered_df_star)
    else:
        st.write("Select a rating range and click 'Apply Filter' to filter the data.")
    

    min_price = st.number_input("Enter minimum price:", min_value=0, value=0, step=50)
    max_price = st.number_input("Enter maximum price:", min_value=0, value=2000, step=50)

    if st.button("Apply"):
        if min_price <= max_price:
            filtered_data['Price'] = pd.to_numeric(filtered_data['Price'], errors='coerce')
            filtered_data = filtered_data.dropna(subset=['Price'])
            filtered_df_price = filtered_data[(filtered_data['Price'] >= min_price) & (filtered_data['Price'] <= max_price)]
            st.write("Filtered data based on price range:", filtered_df_price)
        else:
            st.write("Please enter a valid price range. Minimum price should be less than or equal to maximum price.")
    else:
        st.write("Click 'Apply' to select a price range and filter the data.")

    available = st.selectbox("Choose Availability:", ['Select Availability', 'Available', 'Filling Fast'])
    if available != 'Select Availability':
        filtered_data['Seat_Availability'] = filtered_data['Seat_Availability'].apply(
                    lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0
            )
        if available == 'Filling Fast':
                filtered_df_av = filtered_data[filtered_data['Seat_Availability'] < 5]
        else:
                filtered_df_av = filtered_data[filtered_data['Seat_Availability'] > 5]
        if filtered_df_av.empty:
                st.write("No bus available.")
        else:
                st.write(filtered_df_av)
    

    filtered_data['Departing_Time'] = pd.to_datetime(filtered_data['Departing_Time']).dt.time
    start_time = st.time_input("Select start time:")
    end_time = st.time_input("Select end time:")

    if st.button("Apply", key="apply_button"):
        if start_time < end_time:
            filtered_df_depart = filtered_data[(filtered_data['Departing_Time'] >= start_time) & (filtered_data['Departing_Time'] <= end_time)]
            if not filtered_df_depart.empty:
                st.write("Filtered data based on time range:", filtered_df_depart)
            else:
                st.write("No buses available at this range of time.")
        else:
            st.write("Please make sure the start time is earlier than the end time.")
    





        






    


