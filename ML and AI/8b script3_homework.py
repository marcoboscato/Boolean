#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Boolean Data Analytics Course

Web Scraping and Web Interaction with Selenium: 
    Homework Exercises
"""


### 0. 
### RUN THIS INITIAL SETUP CODE

# Download the latest stable release of the ChromeDriver
# https://sites.google.com/chromium.org/driver/

# import requred libraries and modules
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import seaborn as sns

# # initialise the driver (and open up a browser window)
driver = webdriver.Chrome()

# open up a specific web page
driver.get("https://www.scrapethissite.com/pages/forms/")


# since we will need to repeat this process for other 5 variables, 
# let's create a function
def create_col(class_name):
    s_column = driver.find_elements(By.CLASS_NAME, class_name)
    column = [col.text for col in s_column]
    return column


def scrape_page(page):
    # click on first page
    driver.find_elements(By.LINK_TEXT, str(page))[0].click()
    
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


###########################################################################

### 1.
### USING THE HTML ELEMENTS FROM THE www.scrapethissite.com/pages/forms/ 
### WEB PAGE, CREATE A LIST "pages" CONTAINING ALL THE PAGES AVAILABLE
### IN THE PAGINATION SECTION (eg: [1,2,3,4,...]) 





### 2. 
### INITIALISE AN EMPTY DATAFRAME HAVING THE CORRECT COLUMN NAMES BUT WITH 
### NO DATA INSIDE, CALL it "df_teams"





### 3.
### USING THE FUNCTION "scrape_page()" WE CREATED ABOVE, LOOP THROUGH ALL THE 
### PAGES AVAILABLE (see question 1.) AND APPEND EACH RESULTING DATAFRAME
### TO THE "df_teams" DATAFRAME YOU JUST INITIALISED





### 4. 
### RE-INDEX THE FINAL DATAFRAME "df_teams" YOU JUST CREATED





### 5. 
### a. USING SEABORN, PRODUCE A COUNTPLOT THAT SHOWS THE NUMBER OF TEAMS 
###    IN THE DATASET AVAILABLE FOR EACH YEAR 
### b. THE NUMBER OF TEAMS IN THE LEAGUE HAVE BEEN INCREASING IN THE PAST, 
###    IN WHICH YEAR DID THEY BEGIN TO REACH A STABLE NUMBER?





### 6. 
### a. WHICH TEAM WON MORE GAMES IN 2011? IF THERE ARE ANY TIES, USE THE 
###    NUMBER OF GOALS SCORED VARIABLE TO "BREAK THEM"
### b. HOW MANY WERE GOALS SCORED BY THIS TEAM?
### c. WAS IT ALSO THE TEAM THAT SCORED THE HIGHEST NUMBER OF GOALS? 





### 7. 
### IF YOU HAVEN'T NOTICED YET, THE COLUMN'S DATA TYPES ARE NOT CORRECT 
### FOR SOME VARIABLES. FIX THE COLUMN'S DATA TYPES AS YOU SEE FIT.





### 8. 
### USING SEABORN, MAKE A LINE PLOT THAT SHOWS THE TREND OF THE 
### NUMBER OF WINS FOR EACH YEAR FOR THE TEAM YOU FOUND AT QUESTION 6.





###########################################################################
### ADVANCED PART (THINGS WE HAVEN'T SEEN TOGETHER)
###########################################################################


### 9. 
### USING SELENIUM, GO TO THE "https://www.scrapethissite.com/pages/forms/"
### PAGE AND (STILL USING SELENIUM, NOT THE MOUSE AND KEYBOARD) TYPE IN THE 
### SEARCH BOX THE NAME OF A TEAM OF YOUR CHOICE AND SCRAPE THE DATA FROM 
### THE RESULTING TABLE. SAVE THE DATA IN A NEW DF NAMED "df_teams_query"





### 10. 
### CREATE A NEW SCRIPT THAT DOES THE SAME THINGS WE DID FROM QUESTION 0. TO 
### QUESTION 4. BUT THIS TIME SELECTING 100 RESULTS PER PAGE (INSTEAD OF THE 
### CURRENT 25 RESULTS PER PAGE). 





