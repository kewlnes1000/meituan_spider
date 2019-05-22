import configparser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


config = configparser.ConfigParser()
config.read('config/config.ini', encoding='UTF-8')
chrome_path = config.get("option", "chrome_path")
phone = config.get("option", "phone")

mobileEmulation = {'deviceName': 'iPhone 6/7/8 Plus'}
options = webdriver.ChromeOptions()
options.add_argument('lang=zh-tw.UTF-8')
options.add_experimental_option('mobileEmulation', mobileEmulation)
driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=options)

driver.set_window_position(0, 0)  # 瀏覽器位置
driver.set_window_size(375, 900)  # 瀏覽器大小
driver.implicitly_wait(10)  # seconds
driver.get("https://h5.waimai.meituan.com/login")
wait = WebDriverWait(driver, 10)

phoneNumInput = driver.find_element_by_xpath('//*[@id="phoneNumInput"]')
phoneNumInput.send_keys(phone)

sendCodeBtn = driver.find_element_by_xpath('//*[@id="sendCodeBtn"]')
sendCodeBtn.click()

yodaBox = driver.find_element_by_xpath('//*[@id="yodaBox"]')
action = ActionChains(driver)
action.click_and_hold(yodaBox).perform()
action.move_by_offset(xoffset=250, yoffset=0).perform()
action.release(yodaBox).perform()


def get_track(self, distance):
    track = []
    current = 0
    mid = distance*3/4
    t = random.randint(2, 3)/10
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0+a*t
        move = v0*t+1/2*a*t*t
        current += move
        track.append(round(move))
