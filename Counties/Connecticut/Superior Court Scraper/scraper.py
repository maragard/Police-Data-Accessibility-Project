import argparse
import re
import requests as req
from bs4 import BeautifulSoup as BS, SoupStrainer
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

url = "https://civilinquiry.jud.ct.gov/PartySearch.aspx"

def has_id(tag):
    return tag is not None

def gather_cases():
    docket_filter = SoupStrainer("a", id=has_id)

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)

    finder = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtLastName")
    finder.send_keys("Police Department")

    search_select = Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlLastNameSearchType"))
    search_select.select_by_value("Contains")

    submit = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnSubmit"]')
    submit.click()

    populate_wait = WebDriverWait(driver, 60).until(lambda x: x.find_element_by_id("ctl00_ContentPlaceHolder1_gvPartyResults"))

    # soup = BS(driver.page_source, 'lxml', parse_only=docket_filter)
    
    driver.quit()

    # links = [f"https://civilinquiry.jud.ct.gov/{tag['href']}" for tag in soup('a') if re.search(r'_hlnkDocketNo', tag['id']) is not None]

    # dupe_fix = {x: None for x in links}
    # links = dupe_fix.keys()
    # print(links) 


if __name__ == "__main__":
    gather_cases()