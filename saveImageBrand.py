import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from tqdm import tqdm
from PIL import Image
import requests 

models = np.loadtxt('./CarBrands.txt', dtype=str)
driver = webdriver.Chrome(executable_path="/home/mohammadhasan/MyCodes/ChromeDriver/chromedriver")
counter = 0

def scroll_end():
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(2)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

for i in tqdm(range(14, len(models))):

    link_list = []

    driver.get(f'https://bama.ir/car/{models[i]}?image=1')
    scroll_end()
    list_of_Links = driver.find_elements(By.CSS_SELECTOR,'#__layout > div > div > section > div.bama-adlist-content-holder > div > div.bama-ad-holder')

    for e in list_of_Links:
        link_list.append(e.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

    for link in link_list:
        img_list=[]
        temp_array = []
        driver.get(link)
        time.sleep(1)

        image_element = driver.find_elements(By.CSS_SELECTOR, '#main-slider > div:nth-child(2) > ul > li')

        for e in image_element:
            img_url = e.find_element(By.CSS_SELECTOR,'div > img').get_attribute('src')
            if img_url is not None:
                img_url = img_url.replace('_thumb_240_160.jpg', '_thumb_900_600.jpg')
                temp_array.append(img_url)
        
        for x in temp_array:
            if x not in img_list:
                img_list.append(x)

        if not os.path.exists(f"./CarImage_iran/{i+1}-{models[i]}"):
            os.makedirs(f"./CarImage_iran/{i+1}-{models[i]}")

        for j in range(len(img_list)):
            try:
                time.sleep(1)
                path = f"./CarImage_iran/{i+1}-{models[i]}/{models[i]}-{counter}.jpg"
                img = Image.open(requests.get(img_list[j], stream = True).raw)
                img.save(path)
                counter +=1

            except:
                print(img_list[j])
                print('Error in saving image')