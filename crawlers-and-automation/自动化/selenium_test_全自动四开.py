

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import threading

url = "https://bahuyun.com/bdp/form/1376331928812650496"


class SeleniumTest:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def shezhi(self):
        opt = Options()
        opt.add_argument("--no-sandbox")
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_experimental_option('detach', True)
        driver = webdriver.Edge(options=opt)
        driver.set_window_position(self.x,self.y)
        driver.set_window_size(400,600)
        driver.get(url)
        driver.implicitly_wait(10)
        return driver

    def tijiao(self):
        driver = self.shezhi()
        for i in range(3):
            driver.find_element(By.XPATH, '//input[@id="van-field-1-input"]').send_keys("柳泽楷")
            driver.find_element(By.XPATH, '//input[@id="input-c-Mhri5HdmyRkWDcJfe5p"]').send_keys("00202503019")
            driver.find_element(By.XPATH, '//*[@id="my-node"]/div[4]/div/div[2]/div/div/div/select/option[2]').click()
            driver.find_element(By.XPATH, '//div[6]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//i[1]').click()
            driver.find_element(By.XPATH, '//div[4]//div[1]//i[1]').click()
            driver.find_element(By.XPATH, '//div[5]//div[1]//i[1]').click()
            driver.find_element(By.XPATH, '//div[7]//div[1]//i[1]').click()
            driver.find_element(By.XPATH, '//*[@id="my-node"]/div[9]/div/div[2]/div/div[1]/div[2]/div[5]/i').click()

            sleep(2)

            driver.find_element(By.XPATH, '//button[@id="submit-button"]').click()
            sleep(2)
            driver.find_element(By.XPATH, '//div[3]//button[1]').click()

            windows = driver.window_handles
            driver.close()
            driver.switch_to.window(windows[1])

st1=SeleniumTest(0,0)
st2=SeleniumTest(500,0)
st3=SeleniumTest(0,700)
st4=SeleniumTest(500,700)
threading.Thread(target=st1.tijiao).start()
threading.Thread(target=st2.tijiao).start()
threading.Thread(target=st3.tijiao).start()
threading.Thread(target=st4.tijiao).start()