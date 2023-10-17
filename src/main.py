from datetime import datetime
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# ROOTPAGE = "https://www.ubisoft.com/ko-kr/search?gss-q="
# GAMESCRICE = "Assassin's Creed"
URL = "https://www.ubisoft.com/ko-kr/game/assassins-creed/all-games"

def go_page(driver:webdriver, url:str)-> None:
    """move page

    Args:
        driver (webdriver): your webdriver
        url (str): you wanted site url
    """
    driver.get(url)
    sleep(10)


options = webdriver.FirefoxOptions()
options.add_argument('--headless')
web = webdriver.Firefox(options=options)

go_page(web, URL)

page_source = web.page_source


soup = bs(page_source, "html.parser")
promo_list = soup.find_all(attrs={'class':'promo__wrapper'})

url = promo_list[0].find(attrs={'class':'promo__wrapper__content'}).find('a')['href']
url = url.replace("/buy", "")

go_page(web, url)

web.quit()