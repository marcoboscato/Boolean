# -*- coding: utf-8 -*-
"""
Boolean Data Analytics Course

Web Scraping and Web Interaction with Selenium: 
 in this script we write some code that looks at the pagination 
 of the website; we create a function that, given a page, 
 navigates to that page and scrapes the data contained in a table
 and then appends it to a previously initialised DataFrame 
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

# open up a specific web page
driver.get("https://www.scrapethissite.com/pages/forms/")


### DEFINE FUNCTION FOR COLUMN LIST CREATION

# since we will need to repeat this process for other 5 variables, 
# let's create a function
def create_col(class_name):
    s_column = driver.find_elements(By.CLASS_NAME, class_name)
    column = [col.text for col in s_column]
    return column


### DEFINE FUNCTION FOR PAGE SCRAPING

def scrape_page(page):
    # click on first page
    # driver.find_element(By.LINK_TEXT, str(page)).click()
    driver.find_element(By.XPATH, f'//*[@id="hockey"]/div/div[5]/div[1]/ul/li[{page+1}]/a').click()
    
    # create a list for each column of the table
    names = create_col('name')
    year = create_col('year')
    wins = create_col('wins')
    losses = create_col('losses')
    goals_for = create_col('gf')
    goals_against = create_col('ga')
    
    # create a temporary DataFrame to store the current page
    df_teams_tmp = pd.DataFrame(
        {'names': names, 
         'year': year,
         'wins': wins, 
         'losses': losses, 
         'goals_for': goals_for, 
         'goals_against': goals_against
         })
    
    return df_teams_tmp


### USE FUNCTION TO RETRIEVE DATA OF A CERTAIN PAGE AND APPEND IT TO DF

# append (with pd.concat()) the temp DataFrame to the empty one
df_teams = scrape_page(1)

df_teams = pd.concat([df_teams, scrape_page(3)])

# re-index the DataFrame to avoid having duplicates in the index
df_teams.index = pd.RangeIndex(len(df_teams.index))

# //*[@id="hockey"]/div/div[5]/div[1]/ul/li[1]/a --> back
# //*[@id="hockey"]/div/div[5]/div[1]/ul/li[2]/a -->page 1
# //*[@id="hockey"]/div/div[5]/div[1]/ul/li[3]/a -->page 2
