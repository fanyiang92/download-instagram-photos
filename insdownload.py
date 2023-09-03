import os
import time
from selenium.webdriver.chrome.options import Options  # 选项功能
import requests
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}
#url = 'https://www.instagram.com/p/CtTmD-AObNp/?igshid=MzRlODBiNWFlZA%3D%3D'
""" PLEASE PASTE YOUR LINK HERE!!! """
url = 'paste your link here!!!'  # paste your link here!!!

def get_next():  #get next page
    button = driver.find_element(By.XPATH, '//div[@class=" _9zm2"]')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(1)

def get_first_page(): #get the information of first page
    url = driver.find_element(By.XPATH, '//*[@class="_acay"]/li[2]/div/div/div/div/div/img').get_attribute('src')
    return url
    time.sleep(2)

def get_other_pages(): #get the information of other pages
    url_2 = driver.find_element(By.XPATH, '//*[@class="_acay"]/li[3]/div/div/div/div/div/img').get_attribute('src')
    return url_2

if __name__ == '__main__':
    if not os.path.exists('ins-img'):  #如果当前路径没有存放图片的文件夹,则创建一个
        os.mkdir('ins-img')
    """添加无头模式,免开浏览器"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    #driver.maximize_window()
    driver.implicitly_wait(20)
    time.sleep(5)

    #pic_url = driver.find_element(By.XPATH, '//*[@class="_acay"]/li[2]/div/div/div/div/div/img').get_attribute('src')
    pic_url = get_first_page()
    print(pic_url)
    pic_url_list = pic_url.split('/')
    pic_url_list_1 = pic_url_list[5].split('?')[0] #获取jpg文件名
    print(pic_url_list_1)
    response = requests.get(url = pic_url, headers=headers)
    with open(f'ins-img/{pic_url_list_1}.jpg', mode='wb') as f:
        f.write(response.content)
    print('已经下载完成第1张')
    #
    #用while True 遍历所有"下一页",当到最后一页时,会报错,此时使用try-except用break 即可.
    while True:
        try:
            # for i in range(2,8):
            get_next()
            pic_url_other = get_other_pages()
            print(pic_url_other)
            other_url_list = pic_url_other.split('/')
            other_url_list_1 = other_url_list[5].split('?')[0]
            response = requests.get(url=pic_url_other, headers=headers)
            with open(f'ins-img/{other_url_list_1}.jpg', mode='wb') as f:
                f.write(response.content)
            print(f'已经下载完成{other_url_list_1}')

        except Exception as e:
            print(e)
            break



    print('=====下载完成=====')
    driver.quit()
