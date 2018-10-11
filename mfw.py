# -*- coding: utf-8 -*-

# import logging
from selenium import webdriver
import schedule, time


def sche_job():
    try:
        print("--Sign process start--")
        driver = webdriver.Chrome()
        driver.get("https://passport.mafengwo.cn/")
        # 登录
        driver.find_element_by_xpath(".//input[@placeholder='您的邮箱/手机号']").send_keys("phone")
        driver.find_element_by_name("password").send_keys("password")
        driver.find_element_by_xpath(".//form[@id='_j_login_form']/div/button").submit()
        # 全局等待
        driver.implicitly_wait(20)
        # 打卡
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element_by_id("head-btn-daka").click()
        # elem1 = driver.find_element_by_id("head-btn-daka")
        # print("id:", elem1)
        #
        # elem2 = driver.find_element_by_xpath(".//div[@class='login-info']/div[@class='head-daka']/a").send_keys("phone")
        # print("xpath:", elem2)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        print("--Sign process end--")
    except Exception as e:
        print("--Error:", e)



schedule.every().day.at("9:35").do(sche_job)
while True:
    schedule.run_pending()
    time.sleep(1)
