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

'''
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
from selenium import webdriver

import json
import requests
'''

# input and page string
coin_name = input("Which coin do you want to check?: ")
coin_name = coin_name.lower().strip().replace(' ', '-')

coin_code = input("What is the code of the coin?: ")
coin_code = coin_code.upper().strip()

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

# 3. historical data 
def getHistoricalData():
    try: 
        print("\n3. Historical data:")
        # initialise scraper without time interval for max historical data
        scraper = CmcScraper(coin_code)
        # Pandas dataFrame for the same data
        df = scraper.get_dataframe()
        print(df)
    except Exception as e: 
        print("Hmm, can't quite find your coin or the data not available on CMC, check and run again?")


# 4. check scam
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

        print("\n4. Scam check: ")
        scoreValues(safety_score)
    except Exception as e: 
        print("Hmm, can't quite find your coin or the data not available on isthiscoinascam.com, check and run again?")

    
# main
def main():
    printDateAndTime()
    getPrice()
    getRank()
    getHistoricalData()
    checkScam()
    exit = input("\n Enter any key if you want to exit: ")


if __name__ == "__main__":
    main()