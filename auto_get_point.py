# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
import json
import sys

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
        driver.get(r'https://shopee.tw/')
        # login(driver)
    elif options == 2:
        login(driver)
        renew_shopee_cookies_file(driver)
        print('save cookies done')


def login(driver):
    # login to Shopee
    driver.get(r'https://shopee.tw/')

    time.sleep(2)
    # send esc key for skip AD
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # element = driver.find_element_by_class_name('navbar__link--account')
    time.sleep(2)
    # click login button
    element = driver.find_element_by_xpath("//div[@id='main']/div/div[2]/div[1]/div/div[1]/div/ul/li[5]")
    element.click()

    # press TAB key for into user name field
    tab_num = 0
    while tab_num < 14:
        webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
        tab_num += 1
        time.sleep(0.2)

    pyautogui.typewrite(username)
    pyautogui.press('tab')
    pyautogui.typewrite(password)


def renew_shopee_cookies_file(driver):
    print("After 30 sec. will store cookie to cookie")
    time.sleep(30)
    driver.refresh()
    time.sleep(5)

    cookies = driver.get_cookies()
    json_cookies = json.dumps(cookies)
    with open('cookies.json', 'w') as f:
        f.write(json_cookies)


def load_cookies(driver):
    # driver.delete_all_cookies()
    driver.get(r'https://shopee.tw/')
    time.sleep(2)
    # send esc key for skip AD
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    with open('cookies.json', 'r', encoding='utf-8') as f:
        list_cookies = json.loads(f.read())

    count = 0
    for cookie in list_cookies:
        count += 1
        print(count)
        if cookie['expiry']:
            expiry = cookie['expiry']
        else:
            expiry = None
        driver.add_cookie({
            'domain': cookie['domain'],
            'httpOnly': cookie['httpOnly'],
            'secure': cookie['secure'],
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expiry': expiry
            # 'expires': cookie['expiry']
        })
    print(list_cookies)

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

    driver.close()
