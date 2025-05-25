from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pickle

driver = webdriver.Chrome()
driver.get('https://www.semrush.com/analytics/organic/pages/?sortField=trafficPercent&db=tr&q=bigbagal.com&searchType=domain')

with open("cookies.json", "r", encoding="utf-8") as f:
    cookie_data = json.load(f)

with open("cookies.pkl", "wb") as f:
    pickle.dump(cookie_data, f)

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    # Remove expiry if present (avoids selenium bug)
    cookie.pop('expiry', None)
    driver.add_cookie(cookie)

WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@data-ui-name="Box"][@role="row"][@data-at="table-row"]')))
elems = driver.find_elements(By.XPATH, '//*[@data-ui-name="Box"][@role="row"][@data-at="table-row"]')

pages = {}
i = 0
for elem in elems:
    text = elem.get_attribute("innerText")
    text = text.split('\n')
    page = text[0]
    pages[i] = {
        'page':page
    }
    i+=1

for page_number in pages:
    page = pages[page_number]['page']
    driver.get('https://www.semrush.com/analytics/organic/overview/?db=tr&q=https://'+page+'&searchType=url')
    time.sleep(5)
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="classic-research"]/div/div/div[2]/div/div[1]/nav/button[2]')))
    button = driver.find_element(By.XPATH, '//*[@id="classic-research"]/div/div/div[2]/div/div[1]/nav/button[2]')    
    button.click()    
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*/div[2]/div/div/div[2]/div[1]/a/span')))
    elems = driver.find_elements(By.XPATH, '//*/div[2]/div/div/div[2]/div[1]/a/span')
    keywords = []
    for elem in elems:
        text = elem.get_attribute("innerText")
        keywords.append(text)
    ','.join(keywords)
    pages[page_number]['keywords'] = keywords
    button = driver.find_element(By.XPATH, '//*/div[2]/div/div/div[2]/div[1]/a')    
    button.click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//body').send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.XPATH, '//body').send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.XPATH, '//body').send_keys(Keys.PAGE_DOWN)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="serp-analysis"]/div/div/div/div/div/div/div/div/div/div[2]/div/div/a[1]/span')))
    elems = driver.find_elements(By.XPATH, '//*[@id="serp-analysis"]/div/div/div/div/div/div/div/div/div/div[2]/div/div/a[1]/span')
    best_pages = []
    for elem in elems:
        text = elem.get_attribute('innerText')
        best_pages.append(text)
    pages[page_number]['best_pages'] = best_pages
    

print(pages)
    
with open('datas.txt','w',encoding='utf-8') as file:
    for page_number in pages:
        json_line = json.dumps({page_number: pages[page_number]}, ensure_ascii=False)
        file.write(json_line + '\n')