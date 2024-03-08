import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import pytz
from urllib.parse import urlparse
from domainextraction import getDomain
import json
import csv
import pandas as pd
from urllib.parse import urlparse

# Get the current date and time in UTC timezone
utc_now = datetime.datetime.now(tz=pytz.utc)
# Convert UTC to Germany timezone
germany_tz = pytz.timezone('Europe/Berlin')
germany_now = utc_now.astimezone(germany_tz)
# Format the timestamp string
timestamp = germany_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')


#ser = Service(r"/Users/burce/Documents/Development/chromedriver_mac64")
#op = webdriver.ChromeOptions()
#chrome_driver_path = "/Users/burce/Documents/Development/chromedriver_mac_arm64" # the bridge between selenium and chrome
#driver = webdriver.Chrome(service=ser, options=op)

driver = webdriver.Firefox()


def open_browser(URL):
    driver.get(URL)
    driver.implicitly_wait(30)


def get_list_items():
    list_items = driver.find_elements(By.CSS_SELECTOR, '#mbfc-table a')
    new_tabs_list = []
    for list_item in list_items:
        new_tab = {'href': list_item.get_attribute("href"), 'status': 'to-be-retrieved'}
        new_tabs_list.append(new_tab)
    return new_tabs_list

item_dict_list = []
def get_links(new_tabs_list, writer): ## new_tabs_list is the list of all hrefs. the script will open them and get the source url, and other characteristics
    for new_tab in new_tabs_list:
        if new_tab['status'] == 'to-be-retrieved':
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(new_tab['href'])
            driver.implicitly_wait(5)
            try:
                domain = driver.find_element(By.XPATH, '//p[contains(text(), "Source: ")]/a').get_attribute("href")
            except:
                try:
                    domain = driver.find_element(By.XPATH, '//p[contains(text(), "Source:")]/a').get_attribute("href")
                except:
                    try:
                        domain = driver.find_element(By.XPATH, '//p[contains(text(), "Source") and contains(., ":")]/a').get_attribute("href")
                    except:
                        try:
                            domain = driver.find_element(By.XPATH,
                                                     '//span[contains(text(), "Source") and contains(., ":")]/a').get_attribute(
                            "href")
                        except:
                            try:
                                domain = driver.find_element(By.XPATH,
                                                             '//p[contains(., "Source:")]/a').get_attribute(
                                    "href")
                            except:
                                domain = f'There was a problem with finding domain. f{new_tab}'
            item_dict = {'domain': getDomain(domain)}
            item_dict.update({'source': 'mbfc (conspiracy-pseudo-science)'})
            try:
                images = conspiracy_level = driver.find_elements(By.CSS_SELECTOR, 'h1 img')
                for image in images:
                    level = image.get_attribute('data-image-title')
                    if 'con' in str(level):
                        item_dict.update({'conspiracy level': int(level.split('con')[1])})
                    else:
                        if 'pseudo' in str(level):
                            item_dict.update({'pseudo-science level': int(level.split('pseudo')[1])})
                        else:
                            if 'MBFC' in str(level):
                                item_dict.update({'factual reporting level': level.split('MBFC')[1]})
            except:
                try:
                    print("There was an error, tried h2")
                    images = driver.find_elements(By.CSS_SELECTOR, 'h2 img')
                    for image in images:
                        level = image.get_attribute('data-image-title')
                        if 'con' in str(level):
                            item_dict.update({'conspiracy level': int(level.split('con')[1])})
                        else:
                            if 'pseudo' in str(level):
                                item_dict.update({'pseudo-science level': int(level.split('pseudo')[1])})
                            else:
                                if 'MBFC' in str(level):
                                    item_dict.update({'factual reporting level': level.split('MBFC')[1]})
                except:
                    try:
                        print("There was another error, tried .entry-content")
                        images = driver.find_elements(By.CSS_SELECTOR, '.entry-content img')
                        for image in images:
                            level = image.get_attribute('data-image-title')
                            if 'con' in str(level):
                                item_dict.update({'conspiracy level': int(level.split('con')[1])})
                            else:
                                if 'pseudo' in str(level):
                                    item_dict.update({'pseudo-science level': int(level.split('pseudo')[1])})
                                else:
                                    if 'MBFC' in str(level):
                                        item_dict.update({'factual reporting level': level.split('MBFC')[1]})
                    except:
                        print(f'There was a problem with getting the source data {new_tab}')
            item_dict.update({'timestamp': timestamp})
            item_dict_list.append(item_dict)
            new_tab['status'] = 'retrieved'
            with open('new_tabs_list.json', 'w') as back_up_file:
                json.dump(new_tabs_list, back_up_file)

            print(item_dict)
            writer.writerow(item_dict)
               # writer = csv.writer(output_file)
                #writer.(item_dict)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    print(item_dict_list)

        ###you need to make a list again.

# def accept_cookies():
#     try:
#          consent_button = driver.find_element(By.XPATH, '// *[ @ id = "SHORTCUT_FOCUSABLE_DIV"] / div[3] / div / section / div / section[2] / section[1] / form / button')
#             #consent_button = driver.find_element(By.LINK_TEXT, "Accept all")
#          consent_button.click()
#          driver.implicitly_wait(30)
#     except:
#         print('Error while accepting cookies')

# driver.execute_script("window.open('');")
#         driver.switch_to.window(driver.window_handles[-1])
#         driver.get(list_item.get_attribute("href"))
#         driver.implicitly_wait(30)
#         # item_dict = {'title': list_item.text, 'mbfc_page': list_item.get_attribute("href")}
#         print(list_item.get_attribute("href"))
#         try:
#             conspiracy_level = driver.find_element(By.CSS_SELECTOR, 'h1 img').get_attribute('data-image-title')
#         except:
#             try:
#                 print("There was an error, tried h2")
#                 conspiracy_level = driver.find_element(By.CSS_SELECTOR, 'h2 img').get_attribute('data-image-title')
#             except:
#                 print("There was another error, tried .entry-content")
#                 conspiracy_level = driver.find_element(By.CSS_SELECTOR, '.entry-content img').get_attribute(
#                     'data-image-title')
#         print(conspiracy_level)
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])