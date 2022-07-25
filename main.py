import time
import os
import logging
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Disable unsightly webdriver-manager log messages
logging.getLogger('WDM').setLevel(logging.NOTSET)

chrome_options = Options()

# Include this to remove GUI
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")

DL_PATH = os.path.dirname(os.path.realpath(__file__)) + '/assets/'

# continues when the download is finished
def dlwait(path):
    seconds = 0
    dl_wait = True
    while dl_wait: # and seconds < 20:
        time.sleep(1)
        dl_wait = False
        
        for book in os.listdir(path):
            if book.endswith('.crdownload'):
                dl_wait = True
        
        seconds += 1
    return seconds

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Enable downloads in selenium
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': 'assets/'}}
command_result = driver.execute("send_command", params)

# Search and init download
search = "Siddartha"

start_url = f"https://b-ok.cc/s/{search}"

# search results
sresults = []

driver.get(start_url)

anchor_tags = driver.find_elements(By.TAG_NAME, "a")

# loop through anchor tags 
for el in anchor_tags:
    # element's href
    href = str(el.get_attribute('href'))
    
    # if href refers to a book, log it as a search result
    if '/book/' in href:
        sresults.append(href)

result_count = 2
for x in range(result_count):
    driver.get(sresults[x])
    title = driver.find_element(By.TAG_NAME, 'h1').text
    
    try:
        # book information
        info = driver.find_element(By.CLASS_NAME, "bookDetailsBox").text
    except NoSuchElementException:
        info = "Error receiving book details"
    
    # Split data
    info = info.split("\n")
    
    print(f'[{x+1}] {title}\n')
    
    # find properties in info and list it
    for p in info:
        if ":" in p:
            print("\t", p, end=" ")
        else:
            print(p)

    print()


book = int(input("\nEnter desired download: "))

if book == 0:
    driver.quit()
    sys.exit("No download specified. Exiting..")

# Identify book and click download button
driver.get(sresults[book - 1])

title = driver.find_element(By.TAG_NAME, 'h1').text
driver.find_element(By.CLASS_NAME, "dlButton").click()

dltime = dlwait(DL_PATH)

print(f"Successfully downloaded {title}. \nElapsed time (seconds): {dltime}")
driver.quit()
