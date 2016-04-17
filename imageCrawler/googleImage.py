# -*- coding: utf-8 -*-
__author__ = 'Deplax'

import urllib
import time
import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def getUrl(rawURL):
    pattern = "imgurl=(.*?)&"
    p = re.compile(pattern)
    m = p.search(rawURL)
    return urllib.unquote(m.group(1))

url = "https://google.com/"
query = u"아이유"
elements = ""
urlList = []


print "Google ImageCrawl Start"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent

driver = webdriver.PhantomJS(executable_path="../webdriver/phantomjs", desired_capabilities=dcap)
#driver = webdriver.Chrome(executable_path="../webdriver/chromedriver", desired_capabilities=dcap)
driver.set_window_size(2560, 1600)
print "setting complete"

driver.get(url)
searchBox = driver.find_element_by_css_selector("#lst-ib")
searchBox.send_keys(query, Keys.ENTER)
print "search complete"

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#hdtb-msb > div:nth-child(2) > a")))
imgTabButton = driver.find_element_by_css_selector("#hdtb-msb > div:nth-child(2) > a")
imgTabButton.click()
print "move imageTab"

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#hdtb-msb > div:nth-child(1) > a")))
logo = driver.find_element_by_css_selector("#logo")

print "ajax loading"
try:
    for i in xrange(5):
        logo.send_keys(Keys.END)
        time.sleep(3)
        logo.send_keys(Keys.END)
        more = driver.find_element_by_css_selector("#smb")
        more.click()
except:
    elements = driver.find_elements_by_css_selector("#rg_s > div > a")
    driver.save_screenshot('screen.png')
print "loading complete"


for el in elements:
    href = el.get_attribute("href")
    if href is not None:
        urlList.append(getUrl(href))

driver.close()


def downloadImage(dir, url, i):
    print "download %s : %s" % (str(i).zfill(3), url)
    if url[-4:-3] == ".":
        urllib.urlretrieve(url, dir + str(i).zfill(3) + url[-4:])
    else:
        urllib.urlretrieve(url, dir + str(i).zfill(3) + ".jpg")

i = 0
dir = "images/" + query + "/"
if not os.path.exists(dir):
    os.makedirs(dir)

for url in urlList:
    try:
        downloadImage(dir, url, i)
    except:
        print "fail :" + str(i).zfill(3) + " | url : " + url
    i = i + 1