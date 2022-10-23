#import
import bs4
from bs4 import BeautifulSoup as bs
from datetime import datetime
from datetime import date
from unicodedata import normalize
from cryptocmd import CmcScraper

import pandas as pd

pd.set_option('display.max_colwidth', 500)
import time
import requests
import random

# import for selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# input and page string variables
coin_name = input("Which coin do you want to check?: ")
coin_name = coin_name.lower().strip().replace(' ', '-')

coin_code = input("What is the code of the coin?: ")
coin_code = coin_code.upper().strip()

# socials variables
socials = ['Twitter','Facebook','Instagram','t.me','Discord','Reddit']
others = ['medium']
others.append(coin_name)
others.append(coin_code)

# soup 
string_page = "https://coinmarketcap.com/currencies/" + coin_name + "/"
page = requests.get(string_page)
soup = bs(page.content, features="html.parser")

# time and date 
def printDateAndTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today().strftime("%d/%m/%Y")
    print(f'\nAccording to coinmarketcap.com, here is the information for {coin_name} at {current_time} of {today}:\n')

# 1. price 
def getPrice():
    try:
        price = [link.string for link in soup.find_all(class_='priceValue')]
        print("1. Current price:" ,price[0])
    except Exception as e:
        print("1. Current price:")
        print("Hmm, can't quite find your coin to get the price, check and run again?")

# 2. rank
def getRank():
    try:
        rank =  [link.string for link in soup.find_all(class_='namePill namePillPrimary')]
        print("\n2. Current rank:" , rank[0])
    except Exception as e:
        print("\n2. Current rank:")
        print("Hmm, can't quite find your coin to get the rank, check and run again?")


# spores network market

# 3. Socials link
def getSocials():
    s= Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.get(string_page)
    driver.minimize_window()

    # here you can find all the links
    links = driver.find_elements(By.XPATH, '//a[@href]')
    # get attribute links
    href = [i.get_attribute("href") for i in links]
    # remove duplicate links
    href = list(dict.fromkeys(href))
    # remove coinmarketcap links
    href = [item for item in href if "coinmarketcap" not in item.lower()]

    # printing out infos
    print("\n3. Socials links:")

    for substring in socials: 
        if substring == 't.me':
            print("* Telegram links:")
        else:
            print(f"* {substring} links:")
        for i in href:
            if substring.lower() in i:
                print(i)

# 4. historical data 
def getHistoricalData():
    try: 
        print("\n4. Historical data:")
        # initialise scraper without time interval for max historical data
        scraper = CmcScraper(coin_code)
        # Pandas dataFrame for the same data
        df = scraper.get_dataframe()
        print(df)
    except Exception as e: 
        print("Hmm, can't quite find your coin or the data not available on CMC, check and run again?")

# 5. check scam
def scoreValues(str):
    print(f'Total score is: {str[0]}%.')
    print(f'Numbers of critical flags is: {str[1]}.')
    print(f'Numbers of major flags is: {str[2]}.')
    print(f'Numbers of medium flags is: {str[3]}.')
    print(f'Numbers of minor flags is: {str[4]}.')
    print(f'Numbers of info flags is: {str[5]}.')

def checkScam():
    try:      
        string_page = 'https://isthiscoinascam.com/check/' + coin_name
        page = requests.get(string_page)
        soup1 = bs(page.content, features="html.parser")

        # score check
        safety_score =  [link.string for link in soup1.find_all(class_='score_count')]

        print("\n5. Scam check: ")
        scoreValues(safety_score)
    except Exception as e: 
        print("Hmm, can't quite find your coin or the data not available on isthiscoinascam.com, check and run again?")

    
# main
def main():
    printDateAndTime()
    getPrice()
    getRank()
    getSocials()
    getHistoricalData()
    checkScam()
    exit = input("\nEnter any key if you want to exit. Have a nice day :)")


if __name__ == "__main__":
    main()
