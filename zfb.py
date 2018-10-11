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
        browser.get('https://www.taobao.com')
        # 加载需要一定时间的，设置了等待时间，等待加载
        # 输入按钮的加载等待
        input = wait.until(
            # 设置加载目标，它是一个选择器，参数是需要选择方式和等待加载的内容
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))  # 选择CSS选择器和选择内容
        )
        # 提交按钮
        submit = wait.until(
            # EC后面是选择条件，按钮的加载条件最好的是element_to_be_clickable，意思为元素可以点击的
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        input.send_keys(keyword)  # send_keys对输入框输入内容
        submit.click()  # 提交搜索内容，进入下一个页面
        # 等待页码元素加载完成，并返回最大页码数
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        # 等待加载完成后获取信息
        get_products()
        return total.text
    except TimeoutException:
        # 超时后重新请求，因此递归调用
        return search()


def next_page(page_number):
    try:
        # 页码输入框和翻页按钮
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        # 提交按钮
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        # 判断翻页成功
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                              '#mainsrp-pager > div > div > div > ul > li.item.active > span'),
                                             str(page_number)))
        get_products()
    except TimeoutException:
        return next_page(page_number)


def get_products():
    # 判断单个页面是否被加载出来
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source  # 获取页面源代码，所有的
    # 使用BS进行分析
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('#mainsrp-itemlist .items .item')
    for item in items:
        # image = item.select('.pic .img')[0]['data-src']
        price = item.select('.price strong')[0].text
        deal = item.select('.deal-cnt')[0].text[:-3]
        title = item.select('.title')[0].text.strip()
        shop = item.select('.shop')[0].text.strip()
        location = item.select('.location')[0].text
        product = {
            # 'image': image,
            'price': price,
            'deal': deal,
            'title': title,
            'shop': shop,
            'location': location
        }
        save_text(product)  # 下载内容


def save_text(product):
    # # 保存为txt文件，a追加写模式，编码模式utf-8
    # with open('text.txt', 'a', encoding='utf-8') as f:
    #     # 使用JSON把字典转换为str格式，加换行符
    #     f.write(json.dumps(product, ensure_ascii=False) + '\n')
    #     f.close()

    row = [product['image'], product['price'], product['deal'], product['title'], product['shop'], product['location']]
    sheet.append(row)
    wb.save('C:\\Users\\Administrator\\Documents\\sample.xlsx')


def main():
    # 通过关键字在淘宝进行搜索
    total = search('美食')
    # 用正则提取页码数字
    total = 1  # int(re.compile('(\d+)').search(total).group(1))
    # 翻页
    for i in range(2, total + 1):  # 循环包含前，不包含尾
        next_page(i)
    browser.close()


if __name__ == '__main__':
    main()
