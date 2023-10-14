from bs4 import BeautifulSoup as bs
from selenium import webdriver as web
from selenium.webdriver.support.ui import Select
from time import sleep

ASS = 'AC'

# stamp site game url get
def page_move(drvier, urls:list):
    for url in urls:
        page = drvier.get(url)
        driver.find_element('id', 'view_product_page_btn').click()

def find_url(driver)->list:
    page_source = driver.page_source
    soup = bs(page_source, 'html.parser')
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
def click_button(drvier)->None:
    button = driver.find_element("id","filter_app_type_all")
    button.click()
    sleep(1)

# web driver
driver = web.Firefox()
sleep(1)

# driver goto website
driver.get(f'https://store.steampowered.com/developer/{ASS}')
sleep(1)
click_button(driver)
scroll(driver)
game = find_url(driver)

driver.get(game[0])
sleep(1)
select = Select(driver.find_element('id','ageYear'))
select.select_by_value('1980')
driver.find_element('id', 'view_product_page_btn').click()
sleep(1)

driver.quit()