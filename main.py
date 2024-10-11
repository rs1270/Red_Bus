from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Initialize the Chrome WebDriver
def initialize_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

# Load the target webpage
def load_page(driver, url):
    driver.get(url)
    time.sleep(5) 

# Extracts the bus routes displayed on the page
def scrape_bus_routes(driver):
    route_elements = driver.find_elements(By.CLASS_NAME, 'route')
    bus_routes_link = [route.get_attribute('href') for route in route_elements]
    bus_routes_name = [route.text.strip() for route in route_elements]
    return bus_routes_link, bus_routes_name

# Collects the detailed information for each bus on the given route
def scrape_bus_details(driver, url, route_name):
    
            driver.get(url)
            time.sleep(5)  
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5) 

            bus_name_elements = driver.find_elements(By.CLASS_NAME, "travels.lh-24.f-bold.d-color")
            bus_type_elements = driver.find_elements(By.CLASS_NAME, "bus-type.f-12.m-top-16.l-color.evBus")
            departing_time_elements = driver.find_elements(By.CLASS_NAME, "dp-time.f-19.d-color.f-bold")
            duration_elements = driver.find_elements(By.CLASS_NAME, "dur.l-color.lh-24")
            reaching_time_elements = driver.find_elements(By.CLASS_NAME, "bp-time.f-19.d-color.disp-Inline")
            star_rating_elements = driver.find_elements(By.XPATH, "//div[@class='rating-sec lh-24']")
            price_elements = driver.find_elements(By.CLASS_NAME, "fare.d-block")
            seat_availability_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left m-top-30') or contains(@class, 'seat-left m-top-16')]")

            bus_details = []
            for i in range(len(bus_name_elements)):
                bus_detail = {
                    "Route_Name": route_name,
                    "Route_Link": url,
                    "Bus_Name": bus_name_elements[i].text,
                    "Bus_Type": bus_type_elements[i].text,
                    "Departing_Time": departing_time_elements[i].text,
                    "Duration": duration_elements[i].text,
                    "Reaching_Time": reaching_time_elements[i].text,
                    "Star_Rating": star_rating_elements[i].text if i < len(star_rating_elements) else '0',
                    "Price": price_elements[i].text,
                    "Seat_Availability": seat_availability_elements[i].text if i < len(seat_availability_elements) else '0'
                }
                bus_details.append(bus_detail)
            return bus_details
        



all_bus_details = []

# Function to handle page-wise scraping for multiple pages
def scrape_all_pages(driver, URL):
    for page in range(1,4):  
        
            load_page(driver, URL)
            
            if page > 1:
                pagination_tab = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'DC_117_pageTabs')][text()='{page}']"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", pagination_tab)
                driver.execute_script("arguments[0].click();", pagination_tab)
                time.sleep(5) 
            
           
            all_bus_routes_link, all_bus_routes_name = scrape_bus_routes(driver)
            for link, name in zip(all_bus_routes_link, all_bus_routes_name):
                bus_details = scrape_bus_details(driver, link, name)
                if bus_details:
                    all_bus_details.extend(bus_details) 

        

# Scraping for all government bus companies in the list
govt = ['apsrtc', 'rsrtc','uttar-pradesh-state-road-transport-corporation-upsrtc','assam-state-transport-corporation-astc','pepsu','hrtc','wbtc-ctc','bihar-state-road-transport-corporation-bsrtc','south-bengal-state-transport-corporation-sbstc','chandigarh-transport-undertaking-ctu']
driver = initialize_driver()

for i in govt:
    URL = f"https://www.redbus.in/online-booking/{i}"
    scrape_all_pages(driver, URL)

# Converting the final data into a DataFrame
df = pd.DataFrame(all_bus_details)
df.to_csv('govt_bus_detailsfull.csv', index=False)

# Closing the driver
driver.quit()
