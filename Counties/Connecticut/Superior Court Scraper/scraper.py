import argparse
import re
import requests as req
from bs4 import BeautifulSoup as BS, SoupStrainer
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

url = "https://civilinquiry.jud.ct.gov/PartySearch.aspx"

class ConnCourt(AbstractEventListener):

    def __init__(self):
        pass

    def after_navigate_to(url, driver):
        if 'PartySearchResults.aspx' in url:
            pass

def has_id(_attr):
    return _attr is not None

def gather_cases():
    docket_filter = SoupStrainer("a", id=has_id)

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)

    finder = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtLastName")
    finder.send_keys("Police ")

    search_select = Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlLastNameSearchType"))
    search_select.select_by_value("Contains")

    submit = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnSubmit"]')
    submit.click()

    populate_wait = WebDriverWait(driver, 60).until(lambda x: x.find_element_by_id("ctl00_ContentPlaceHolder1_gvPartyResults"))

    pages = driver.find_elements_by_xpath("//a[contains(@href, 'Page$')]")
    print(f"Pages: {(len(pages)/2)+1}")

    links = [tag.get_attribute('href') for tag in driver.find_elements_by_xpath("//a[contains(@href, 'DocketNo=')]")]
    print(len(links)) 

    driver.quit()

if __name__ == "__main__":
    gather_cases()