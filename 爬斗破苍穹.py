# -*-coding=UTF-8-*-

# 目前可能需要改一下才能运行
import requests
from bs4 import BeautifulSoup
import time
import random
import os
from selenium import webdriver
from urllib.request import urlopen


def get_content(my_url):  # 搜索斗破苍穹
    head = {'user_agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'}
    timeout = random.choice(range(80,180))
    my_date = {
        'key': '斗破苍穹',
        'button': '搜索漫画',
    }
    r = requests.post(my_url, headers=head, data=my_date)
    r.encoding = 'utf-8'
    return r.text


def get_link(html_text):  # 打开斗破苍穹并找到177话
    soup = BeautifulSoup(html_text, "html.parser")
    body = soup.body
    data = body.find('div', {'id': 'dmList'})
    ul = data.find('ul')
    li = ul.find_all('li')
    for man in li:
        p = man.find('p')
        a = p.find('a')
        img = a.find('img')
        if img.get('alt') == '斗破苍穹':
            url = 'http://www.chuiyao.com' + a.get('href')
            head = {
                'user_agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'}
            timeout = random.choice(range(80, 180))
            rep = requests.get(url, headers=head, timeout=timeout)
            rep.encoding = 'utf-8'
            bs = BeautifulSoup(rep.text, "html.parser")
            body = bs.body
            data = body.find('div', {'id': 'play_0'})
            ul = data.find('ul')
            li = ul.find_all('li')
            for hua in li:
                a = hua.find('a')
                if a.get('title') == '第177话 刀光剑影':
                    link = a.get('href')
                    return link
            print('未找到第177话 刀光剑影')
            return None


def get_image(url, path):  # 提取图片
    dcap = {"phantomjs.page.settings.userAgent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'}
    driver = webdriver.PhantomJS(
        executable_path='/Users/hy/phantomJS/phantomjs-2.1.1-windows/bin/phantomjs.exe',
        desired_capabilities=dcap,
    )
    driver.get(url)
    time.sleep(random.uniform(3, 4))
    pagesource = driver.page_source
    bs = BeautifulSoup(pagesource, "html.parser")
    body = bs.body
    totalpage = body.find('span', {'id': 'qTcms_TotalPage1'}).string
    print(totalpage)
    for i in range(1, int(totalpage)+1):
        driver.get(url+'?p='+str(i))
        time.sleep(random.uniform(3, 4))
        pagesource = driver.page_source
        bs = BeautifulSoup(pagesource, "html.parser")
        body = bs.body
        div = body.find('div', {'id': 'wdwailian'})
        img = div.find('img')
        src = img.get('src')
        response = urlopen(src)
        imgbytes = response.read()
        with open(path+'/177_page'+str(i)+'.jpg', 'wb') as fp:
            fp.write(imgbytes)
    driver.close()


url = 'http://www.chuiyao.com/search/'
html_text = get_content(url)
image_link = get_link(html_text)
path = 'C:/Users/hy/Desktop/manhua'
os.mkdir(path)
get_image(image_link, path)
