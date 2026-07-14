# -*- coding: utf-8 -*-
"""
Boolean Data Analytics Course

Web Scraping and Web Interaction with Selenium: 
 in this script we navigate to the page of a website where 
 we scrape the data contained in a table 
"""


### GETTING STARTED

# Download the latest stable release of the ChromeDriver
# https://sites.google.com/chromium.org/driver/

# import requred libraries and modules
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


### DRIVER SETUP

# set the path to the ChromeDriver
# path = ''

# initialise the driver (and open up a browser window)
# driver = webdriver.Chrome(path + '/chromedriver')

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)

### PAGE NAVIGATION

# open up a specific web page
driver.get("https://www.scrapethissite.com/")

# click on the sandbox button
driver.find_element(By.LINK_TEXT, 
                    "Explore Sandbox").click()

# alternative way using XPATH
#driver.find_element(By.XPATH, 
#                    "//a[@class='btn btn-lg btn-default']").click()

# click on the second link 
driver.find_element(By.LINK_TEXT, 
                    "Hockey Teams: Forms, Searching and Pagination").click()

# alternative way using XPATH
#driver.find_element(By.XPATH, 
#                    "//a[@href='/pages/forms/']").click()


###########################################################################
### LIST COMPREHENSIONS --> SEE NOTEBOOK
###########################################################################


### SCRAPING TABLE DATA

# find all elements that have class='name' and put them into a list
s_names = driver.find_elements(By.CLASS_NAME, "name")
names = []
for name in s_names: 
    names.append(name.text)

# alternative way of writing a for loop using a "list comprehension"
# names = [name.text for name in s_names] 

# since we will need to repeat this process for other 5 variables, 
# let's create a function
def create_col(class_name):
    s_column = driver.find_elements(By.CLASS_NAME, class_name)
    column = [col.text for col in s_column]
    return column

# create a list for each column of the table
year = create_col('year')
wins = create_col('wins')
losses = create_col('losses')
goals_for = create_col('gf')
goals_against = create_col('ga')


### STRUCTURE IT INTO A DATAFRAME

# now we combine all these lists into a new DataFrame
# then create a temporary DataFrame
df_teams_pg1 = pd.DataFrame(
    {'names': names, 
     'year': year,
     'wins': wins, 
     'losses': losses, 
     'goals_for': goals_for, 
     'goals_against': goals_against
     })


