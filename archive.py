# NOTE Requirements:
#     - selenium
#     - chromium webdriver binary to be installed.
#     - **localhost (jekyll) webserver to be running when using this script.
"""Take a screenshot of the index page and save it to screenshots"""
import os
import time

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:4000/digitalcitizens/")
time.sleep(0.5)
driver.save_screenshot("assets/screenshots/latest.png")
driver.close()