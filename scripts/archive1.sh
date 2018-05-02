# archive1.sh:
# Take screenshot fof jekyll site homepage.
# NOTE Requirements:
#     - selenium
#     - chromium webdriver binary to be installed.
#     - **localhost (jekyll) webserver to be running when using this script.
set -e

# start jekyll server.
bundle exec jekyll serve &

sleep 3
echo "waited 3 seconds..."

# take screenshot of the index page.
echo "executing pyton script to screenshot index page..."
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 << "EOF"
"""Take a screenshot of the index page and save it to screenshots"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

w, h = (1024, 768)
timeout = 20

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
driver.set_window_size(w, h)

# load page wait until page is loaded. give up if timeout is reached.
driver.get("http://127.0.0.1:4000/digitalcitizens/")
try:
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.TAG_NAME, 'footer')))
    print("Page loaded, taking screenshot")
except TimeoutException:
    print("page took too long to load")

# hack to hide scroll bar before screenshot.
driver.execute_script("document.body.style.position = 'fixed';"
                      "document.body.style.width = '%spx'" % w)
# make screenshot.
driver.save_screenshot("assets/screenshots/latest.png")
driver.quit()
EOF

# kill the webserver.
echo "killing jekyll server process $!"
kill $!
exit