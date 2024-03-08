from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import pygame
import time
import re ## this is to use regex

def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

####!!!!!!!!!!####
#### instead of "/Users/burce/Documents/Development/chromedriver", enter the path to chromedriver in your computer
driver = webdriver.Firefox()

def open_browser(URL):
    driver.get(URL)
    driver.implicitly_wait(5)

def accept_cookies(search_engine_name):
    if search_engine_name == 'Google':
        consent_button = driver.find_element(By.CSS_SELECTOR, '#L2AGLb')
        consent_button.click()
        driver.implicitly_wait(5)
    if search_engine_name == 'Bing':
        consent_button = driver.find_element(By.LINK_TEXT, 'Accept')
        consent_button.click()
        driver.implicitly_wait(10)

def browser_search(search_engine_name, search_word):
    try:
        accept_cookies(search_engine_name)
    except:
        pass
    if search_engine_name == 'Google':
        search = driver.find_element(By.CLASS_NAME, "gLFyf")
        #search.click()
        search.send_keys(search_word)
        search.submit()
        # Search.send_keys(Keys.RETURN) ## This was working initially but then it stopped working. So, I use search.submit()
    if search_engine_name == 'Bing':
        search = driver.find_element(By.CSS_SELECTOR,"textarea")
        #search.click()
        search.send_keys(search_word)
        search.submit()
        # Search.send_keys(Keys.RETURN) ## This was working initially but then it stopped working. So, I use search.submit()

def go_to_next_page(search_engine_name):
    if search_engine_name == 'Bing':
        next = driver.find_element(By.XPATH, "//a[@title='Next page']")
        next.click()
    if search_engine_name == 'Google':
        try:
            next = driver.find_element(By.XPATH, "//a[normalize-space()='Next' and not(*)] | //span[normalize-space()='Next' and not(*)]")
            ### Xpath to this item might change. If you get error: go to google.com using google chrome. Select 'next', right
            ### click. Then
            next.click()
        except:
            try:
                next = driver.find_element(By.XPATH, "//*[@id='pnnext']/span[2]")
                ### Xpath to this item might change. If you get error: go to google.com using google chrome. Select 'next', right
                ### click and choose inspect. When you do this, HTML code of the website will be opened and some line(s) will be higlighted.
                ### Again, right click on the higlighted line(s), then click copy > Copy XPath. Then paste it in the line above: next = driver.find_element(By.XPATH, "PASTE-HERE")
                next.click()
            except:
                next = driver.find_element(By.XPATH,
                                           "//a[normalize-space()='Weiter' and not(*)] | //span[normalize-space()='Weiter' and not(*)]")
                next.click()

def get_URLs_in(search_engine_name, how_many_pages, how_many_results, URL_list):
    for times in range(how_many_pages):
        #####if working with Google#####
        if len(URL_list) == how_many_results or len(URL_list) > how_many_results:
            break
        if search_engine_name == 'Google':
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            links = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf a')
            if len(links) == 0:
                try:
                    no_captcha = driver.find_element(By.CLASS_NAME, 'gLFyf')
                    print('No result and no capthca')
                    URL_list = []
                    break
                except:
                    print('There was a problem due to CAPTHCHA. It is recommended to revise the search results when the current process is finished.')
                    URL_list.append(None)
                    play_sound('mixkit-correct-answer-tone-2870.wav')
                    time.sleep(10)
                    break
            else:
                for link in links:
                    href = link.get_attribute('href')
                    URL_list.append(href)
                    if len(URL_list) == how_many_results:
                        break
            try:
                driver.implicitly_wait(10)
                go_to_next_page(search_engine_name)
                print('Next page')
            except:
                print('Could not open the next page. Probably because there is none.')
                break
        ####Using Bing#######
        if search_engine_name == 'Bing':
            driver.implicitly_wait(10)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            links = driver.find_elements(By.CSS_SELECTOR, 'h2 a')
            if len(links) == 0:
                print('No result')
                URL_list = []
                break
            else:
                for link in links:
                    href = link.get_attribute('href')
                    URL_list.append(href)
                    if len(URL_list) == how_many_results:
                        break
                try:
                    driver.implicitly_wait(10)
                    go_to_next_page(search_engine_name)
                    print('Next page')
                except:
                    #####Receiving this message is not bad. The next page is usually not opened because
                    print('Could not open the next page. Probably because there is none.')
                    break

def quit():
    driver.quit()

