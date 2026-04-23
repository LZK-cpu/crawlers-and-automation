from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from lxml import etree

# while True:
#     if datetime.now().strftime('%H:%M:%S').__eq__('12:30:00'):
#         print(datetime.now().strftime('%H:%M:%S'))
#         break

url = "https://www1.szu.edu.cn/v.asp?id=185"


def shezhi():
    opt = Options()
    opt.add_argument("--no-sandbox")
    opt.add_argument('--disable-blink-features=AutomationControlled')
    # opt.add_argument('--headless')
    opt.add_experimental_option('detach', True)
    driver = webdriver.Edge(options=opt)
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(10)
    return driver


driver = shezhi()
# PC
driver.find_element(By.XPATH,
                    '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/p[4]/u/a').click()
# 登录
driver.switch_to.window(driver.window_handles[-1])
driver.find_element(By.ID, 'username').send_keys('2022190036')
sleep(2)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('07010355')
driver.find_element(By.XPATH, '//*[@id="login_submit"]').click()
# 粤海校区
driver.switch_to.window(driver.window_handles[-1])
driver.find_element(By.XPATH, '//*[@id="sportVenue"]/div[1]/div/div[1]').click()

# 乒乓球://*[@id="sportVenue"]/div[2]/div[2]/div[2]/div[9]/div/div[1]/div/img
# 羽毛球://*[@id="sportVenue"]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/img
driver.find_element(By.XPATH, '//*[@id="sportVenue"]/div[2]/div[2]/div[2]/div[9]/div/div[1]/div/img').click()

# 选择第二天
driver.find_element(By.XPATH,'//*[@id="apply"]/div[3]/div[4]/div[2]/label/div[1]').click()

# 15:00-16:00 //*[@id="apply"]/div[3]/div[6]/div[8]/label/div[1]
# 16:00-17:00 //*[@id="apply"]/div[3]/div[6]/div[9]/label/div[1]
driver.find_element(By.XPATH, '//*[@id="apply"]/div[3]/div[6]/div[13]/label/div[1]').click()

# 选择场
driver.find_element(By.XPATH, '//*[@id="apply"]/div[3]/div[10]/div[10]/label/div[1]').click()
# 确认
driver.find_element(By.XPATH, '//*[@id="apply"]/div[3]/div[13]/button[2]').click()

# 同行人
driver.find_element(By.XPATH, '//*[@id="row0myBookingInfosTable"]/td[1]/a[2]').click()
driver.find_element(By.XPATH, '//*[text()="选择同行人"]').click()
driver.find_element(By.XPATH, '//*[text()="请选择..."]').click()
driver.find_element(By.XPATH, '//*[text()="刘欢"]').click()
driver.find_element(By.XPATH, '//*[@id="buttons"]/button[2]').click()
driver.find_element(By.XPATH, '//*[@id="buttons"]/button').click()

money = driver.find_element(By.XPATH, '//*[@id="money"]').text
if money=='0.00':
    driver.find_element(By.XPATH,'//*[@id="row0myBookingInfosTable"]/td[1]/a[3]').click()
    driver.find_element(By.XPATH, '//*[text()="(体育经费)支付"]').click()
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element(By.XPATH, '//*[text()="下一步"]').click()
    driver.find_element(By.XPATH, '//*[@id="password"]').click()
    driver.find_element(By.XPATH, '//*[@class="key-button key-0"]').click()
    driver.find_element(By.XPATH, '//*[@class="key-button key-1"]').click()
    driver.find_element(By.XPATH, '//*[@class="key-button key-0"]').click()
    driver.find_element(By.XPATH, '//*[@class="key-button key-3"]').click()
    driver.find_element(By.XPATH, '//*[@class="key-button key-5"]').click()
    driver.find_element(By.XPATH, '//*[@class="key-button key-5"]').click()
    driver.find_element(By.XPATH,'//*[@id="keybox"]/table/tbody/tr[2]/td[6]/input').click()
    driver.find_element(By.XPATH,'//*[text()="确认支付"]').click()
else:
    driver.find_element(By.XPATH,'//*[@id="row0myBookingInfosTable"]/td[1]/a[3]').click()
    driver.find_element(By.XPATH,'//*[text()="(剩余金额)支付"]').click()
