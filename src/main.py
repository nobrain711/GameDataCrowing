from datetime import datetime
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver as web
from selenium.webdriver.support.ui import Select
from time import sleep

GAMESCRICE = "Assassin's Creed"
PAGEROOT = "https://store.steampowered.com/"

# stamp site game url get
def page_move(drvier, urls:list):
    for url in urls:
        page = drvier.get(url)
        driver.find_element('id', 'view_product_page_btn').click()

# find_url
def find_url(driver)->list:
    click_button(driver)
    scroll(driver)

    soup = get_Page_Source(driver)
    targets = soup.find_all(attrs={'class':'recommendation'})
    result = []
    
    for target in targets:
        result.append(target.find('a')['href'])

    return result

# scroll
def scroll(driver)->None:
    for _ in range(10):
        # moving scroll
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(1)

# find all app button
def click_button(driver)->None:
    button = driver.find_element("id","filter_app_type_all")
    button.click()
    sleep(1)

# Going root page
def root_page(driver):
    driver.get(PAGEROOT)
    sleep(1)
    return driver

def go_page(driver, url:str):
    driver.get(url)
    sleep(5)

    return driver

# searchbox input text
def searching(driver)->str:
    input_tag = driver.find_element("id", "store_nav_search_term")
    input_tag.send_keys(GAMESCRICE)
    sleep(1)

    soup = get_Page_Source(driver)
    url = soup.find('a',{'class':'match match_creator match_v2 match_category_top ds_collapse_flag'})['href']

    return url

# selenium → bs4
def get_Page_Source(driver):
    page_source = driver.page_source
    soup = bs(page_source, 'html.parser')
    
    return soup

def media(soup)->dict:
    main_image = soup.find(attrs={'class':'game_header_image_full'})
    main_image = main_image.get('src')
    soup = soup.find(attrs={'id': 'highlight_player_area'})
    trallers = [video.get('src') for video in soup.find_all('video')]
    imgaes = [image.find('a')['href'] for image in soup.find_all(attrs={'class':'screenshot_holder'})]

    result = {
        'main_image': main_image,
        'tallers': trallers,
        'images':imgaes
    }

    return result
def get_game_info(soup):
    info_box = soup.find(attrs={'class':'details_block'})
    geners = [target.text for target in info_box.find('span') if target.text != ', ']
    publisher = [target.text for target in info_box.find_all(attrs={'class':'dev_row'})[0].find('a')  if target.text != ', ']
    developer =  [target.text for target in info_box.find_all(attrs={'class':'dev_row'})[1].find('a') if target.text != ', ']
    series = [target.text for target in info_box.find_all(attrs={'class':'dev_row'})[2].find('a') if target.text != ', ']
    reg_date = soup.find('b', string='Release Date:').next_sibling
    reg_date = datetime.strptime(reg_date,"%d %b, %Y").strftime("%Y-%m-%d")
    
    if soup.find(attrs={'class':'game_description_snippet'}) == None:
        defulat_game = soup.find(attrs={'class':'glance_details'}).find('a').text
        info = {
            'geners':geners,
            'developer':developer,
            'publisher':publisher,
            'series':series,
            'reg_date':reg_date,
            'defulat_game': defulat_game
        }
    
    else:
        info = {
            'geners':geners,
            'developer':developer,
            'publisher':publisher,
            'series':series,
            'reg_date':reg_date
        }

    return info

def go_game_page(driver, url:str):
    driver.get(url)
    sleep(1)
    select = Select(driver.find_element('id','ageYear'))
    select.select_by_value('1980')
    driver.find_element('id', 'view_product_page_btn').click()
    sleep(3)   

    return driver

def get_data(driver, url:str):
    driver=go_game_page(driver, url)

    soup = get_Page_Source(driver)
    game_title = soup.find(attrs={'class':'apphub_AppName'}).text
    medias = media(soup)
    info = get_game_info(soup)

    data = {
        'title': game_title,
        'media':medias,
        'info':info
    }

    return data

# web driver
driver = web.Firefox()
sleep(1)

driver = root_page(driver)
url = searching(driver)
driver = go_page(driver, url)
page_list = find_url(driver)
game_data = []
for page in page_list:
    temp = get_data(driver,page_list)
    game_data.append(temp)

driver.quit()

df = pd.DataFrame(game_data)
df.to_excel('test.xlsx',index=False)