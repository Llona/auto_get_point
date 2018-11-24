# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
import json
import sys

url = r'https://shopee.tw/'
coin_url = r'https://shopee.tw/shopee-coins'
username = ''
password = ''

option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=option)


def start(options):
    # # start()
    # option = webdriver.ChromeOptions()
    # # option.add_argument('headless')
    # option.add_argument("--start-maximized")
    # driver = webdriver.Chrome(chrome_options=option)
    # # driver.set_window_size(1920, 1080)

    if options == 1:
        load_cookies(driver)
        time.sleep(10)
        driver.get(coin_url)
        time.sleep(10)
        print(driver.page_source)
        # driver.refresh()
        # time.sleep(30)
        # click get coin point button
        # __layout > div > section > div > div.top > div.check-box > div.check-action > div:nth-child(2) > div
        # element = driver.find_element_by_xpath("//div[@id='__layout']/div/section/div/div[1]/div[1]/div[3]/div[2]/div")
        element = driver.find_element_by_class_name("check-action")
        # element = driver.find_element_by_css_selector("div.login-check-btn")
        # element = driver.find_element_by_tag_name("div data-v-3715bb7c")
        print(element)

        element.click()

        time.sleep(30)
        # login(driver)
    elif options == 2:
        login(driver)
        renew_shopee_cookies_file(driver)
        print('save cookies done')


def login(drivers):
    # login to Shopee
    drivers.get(url)

    time.sleep(5)
    # send esc key for skip AD
    webdriver.ActionChains(drivers).send_keys(Keys.ESCAPE).perform()
    # element = driver.find_element_by_class_name('navbar__link--account')
    time.sleep(2)
    # click login button
    element = drivers.find_element_by_xpath("//div[@id='main']/div/div[2]/div[1]/div/div[1]/div/ul/li[5]")
    element.click()

    # press TAB key for into user name field
    tab_num = 0
    while tab_num < 14:
        webdriver.ActionChains(drivers).send_keys(Keys.TAB).perform()
        tab_num += 1
        time.sleep(0.2)

    pyautogui.typewrite(username)
    pyautogui.press('tab')
    pyautogui.typewrite(password)


def renew_shopee_cookies_file(drivers):
    drivers.delete_all_cookies()
    ss = input("please press enter for get cookie file when browser ready")
    print(ss)
    drivers.refresh()
    time.sleep(5)

    cookies = drivers.get_cookies()
    json_cookies = json.dumps(cookies)
    with open('cookies.json', 'w') as f:
        f.write(json_cookies)


def load_cookies(drivers):
    # login to Shopee first for load cookies
    drivers.delete_all_cookies()
    drivers.get(coin_url)
    time.sleep(2)

    with open('cookies.json', 'r', encoding='utf-8') as f:
        list_cookies = json.loads(f.read())

    for cookie in list_cookies:
        if 'expiry' in cookie:
            expiry = cookie['expiry']
        else:
            expiry = None
        drivers.add_cookie({
            'domain': cookie['domain'],
            'httpOnly': cookie['httpOnly'],
            'secure': cookie['secure'],
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expiry': expiry
            # 'expires': cookie['expiry']
        })
    # print(list_cookies)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        print('into 2')
        if sys.argv[1] == 'cookie':
            start(2)
        else:
            print('input parameter error')
    else:
        print('into 1')
        start(1)

    # driver.close()
