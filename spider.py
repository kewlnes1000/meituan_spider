import configparser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
import random


class SeleniumSpider():
    def __init__(self):
        
        # 读取 config
        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini', encoding='UTF-8')
        chrome_path = self.config.get("option", "chrome_path")
        

        # 设定 chrome driver
        mobileEmulation = {'deviceName': 'iPhone 6/7/8 Plus'}
        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh-tw.UTF-8')
        options.add_experimental_option('mobileEmulation', mobileEmulation)
        self.driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=options)

    def login(self):
        self.driver.set_window_position(0, 0)  # 瀏覽器位置
        self.driver.set_window_size(375, 900)  # 瀏覽器大小
        self.driver.implicitly_wait(10)  # seconds
        self.driver.get("https://h5.waimai.meituan.com/login")

        phone = self.config.get("option", "phone")
        phoneNumInput = self.driver.find_element_by_xpath('//*[@id="phoneNumInput"]')
        phoneNumInput.send_keys(phone)

        sendCodeBtn = self.driver.find_element_by_xpath('//*[@id="sendCodeBtn"]')
        sendCodeBtn.click()      
        self.verify_action()

    def get_track(self,distance):
        track=[]
        speed=[]
        current=0
        mid=distance*3/4
        t=random.randint(2,3)/10
        v=0
        while current<distance:
            if current<mid:
                a=2
            else:
                a=-3
            v0=v
            v=v0+a*t
            move=v0*t+1/2*a*t*t
            current+=move
            track.append(round(move))
            speed.append(round(v))
        return [track,speed]

    def verify_action(self):
        yodaBox = self.driver.find_element_by_xpath('//*[@id="yodaBox"]')
        action = TouchActions(self.driver)
        track_list = self.get_track(800)
        
        for index,track in enumerate(track_list[0]):
            action.tap_and_hold(yodaBox,track,0,track_list[1][index]).perform()


if __name__ == '__main__':
    SeleniumSpider().login()