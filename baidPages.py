import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

browser = webdriver.Chrome()
# 浏览器需要多次使用，所以单独拿出来。设置一个最长的等待时间,等待目标加载完成
wait = WebDriverWait(browser, 10)
# 新建excel
wb = Workbook()
wb.create_sheet('stName', index=0)
sheet = wb.active


def search(keyword):
    # wait容易出现加载时间长的问题，因此用try来捕捉异常
    try:
        browser.get('https://www.baidu.com')
        # 加载需要一定时间的，设置了等待时间，等待加载
        # 输入按钮的加载等待
        input = wait.until(
            # 设置加载目标，它是一个选择器，参数是需要选择方式和等待加载的内容
            EC.presence_of_element_located((By.CSS_SELECTOR, "#kw"))  # 选择CSS选择器和选择内容
        )
        # 提交按钮
        submit = wait.until(
            # EC后面是选择条件，按钮的加载条件最好的是element_to_be_clickable，意思为元素可以点击的
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#form > span > input"))
        )
        input.send_keys(keyword)  # send_keys对输入框输入内容
        submit.click()  # 提交搜索内容，进入下一个页面
        get_info()
    except TimeoutException:
        # 超时后重新请求，因此递归调用
        return search()


def get_info():
    # 判断单个页面是否被加载出来
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content_left')))
    html = browser.page_source  # 获取页面源代码，所有的
    # 使用BS进行分析
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('#content_left > div')
    for item in items:
        Title = item.select('h3 > a')
        mainTit = Title[0].text
        subTit = ''
        if len(Title) > 1:
            subTit = Title[1].text

        url = item.select('div.f13 > a.c-showurl')[0].text if len(item.select('div.f13 > a.c-showurl')) > 0 else ''
        evaluate = re.findall(r"\d+\.?\d*", item.select('div.f13 > span.c-pingjia')[0].text) if len(item.select('div.f13 > span.c-pingjia')) > 0 else ''
        info = {
            'mainTit': mainTit,
            'subTit': subTit,
            'url': url,
            'evaluate': int(evaluate[0]) if len(evaluate) > 0 else 0
        }
        print(info)
        save_text(info)  # 下载内容


def save_text(info):
    row = [info['mainTit'], info['subTit'], info['url'], info['evaluate']]
    sheet.append(row)
    wb.save('C:\\Users\\Administrator\\Documents\\sample.xlsx')


def main():
    # 通过关键字进行搜索
    search('删除本地仓库')
    # 翻页
    for i in range(2):  # 循环包含前，不包含尾
        # selenium的xpath用法，找到包含“下一页”的a标签去点击
        browser.find_element_by_xpath("//a[contains(text(),'下一页')]").click()
        # 判断是否加载完成
        wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="page"]/strong/span[2]'), str(i + 2)))
        get_info()
    browser.close()


if __name__ == '__main__':
    main()
