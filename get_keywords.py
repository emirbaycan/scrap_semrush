from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pickle

driver = webdriver.Chrome()
keyword = "çuval"

# keyword analysis page
driver.get('https://www.semrush.com/analytics/keywordoverview/?db=tr&q='+keyword)

with open("cookies.json", "r", encoding="utf-8") as f:
    cookie_data = json.load(f)

with open("cookies.pkl", "wb") as f:
    pickle.dump(cookie_data, f)

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    # Remove expiry if present (avoids selenium bug)
    cookie.pop('expiry', None)
    driver.add_cookie(cookie)

driver.refresh()

time.sleep(5)

# keywords page
driver.get('https://www.semrush.com/analytics/keywordmagic/?q='+keyword+'&db=tr')

#page count
xpath = '/html/body/div[1]/div[6]/main/div/div/div[5]/div/section[2]/div/div/div[2]/div[2]/div[2]/nav/button[4]/span'
WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, xpath)))
elem = driver.find_element(By.XPATH, xpath)
page_count = elem.get_attribute('innerText')
page_count = int(page_count)

keywords = []
i=1

if page_count > 50:
    page_count = 50


while i < page_count:
    # keywords 100
    xpath = '//html/body/div[1]/div[6]/main/div/div/div[5]/div/section[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div/div[2]/a/span'
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elems = driver.find_elements(By.XPATH, xpath)
    
    for elem in elems:
        text = elem.get_attribute("innerText")
        keywords.append(text)
        
    # next button
    xpath = '/html/body/div[1]/div[6]/main/div/div/div[5]/div/section[2]/div/div/div[2]/div[2]/div[2]/nav/button[3]/span/span'
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elem = driver.find_element(By.XPATH, xpath)
    elem.click()
    
    time.sleep(4)
    
    i+=1

print(keywords)

with open(keyword+'_keywords.txt','w',encoding='utf-8') as file:
    data = ','.join(keywords)
    file.write(data)