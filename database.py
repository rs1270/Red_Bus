import mysql.connector
import pandas as pd
import streamlit as st
#connecting to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password='6198')

csv_file = 'govt_bus_detailsfull.csv'
df = pd.read_csv(csv_file)
#setting up cursor
mycursor = mydb.cursor()
mycursor.execute("USE bus_data")

insert_query = """
        INSERT INTO bus_details 
        (Route_Name, Route_Link, Bus_Name, Bus_Type, Departing_Time, Duration, Reaching_Time, Star_Rating, Price, Seat_Availability) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

for i, row in df.iterrows():
        mycursor.execute(insert_query, tuple(row))

tab1, tab2 = st.tabs(["Home", "Data"])
#user query
sql = "SELECT * FROM bus_details WHERE Bus_Name = 'FRESHBUS'"
mycursor.execute(sql)

data= mycursor.fetchall() 
with tab1:
        st.title('Hello')

   
with tab2:
        if data:
            st.table(data)
        else:
            st.write("No data found.")


mydb.commit()

# Close the cursor and connection
mycursor.close()
mydb.close()