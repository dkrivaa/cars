from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

import data


# Set the path to your web driver
driver_path = "C:\\Users\danny\Desktop\chromedriver.exe"
# Create a Service object
chrome_service = Service(driver_path)

# Create a Chrome webdriver with the Service object
browser = webdriver.Chrome(service=chrome_service)

url = 'https://www.yad2.co.il/price-list/search/specific#manufacturer'
browser.get(url)

textbox = browser.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div/form/span/input')
# Perform actions on the text box
textbox.send_keys(1002985)



# Close the browser
browser.quit()
