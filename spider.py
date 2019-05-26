import configparser
from selenium import webdriver
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random
import time
import easing
import requests


class SeleniumSpider():
    def __init__(self):

        # 读取 config
        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini', encoding='UTF-8')
        chrome_path = self.config.get("option", "chrome_path")

        # 设定 chrome driver
        proxy_host = 'localhost'
        proxy_port = 8080
        mobileEmulation = {'deviceName': 'iPhone 6/7/8 Plus'}
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1')
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-gpu')
        options.add_argument('lang=zh-tw.UTF-8')
        options.add_experimental_option('mobileEmulation', mobileEmulation)

        options.add_argument('--proxy-server=%s:%s' % (proxy_host, proxy_port))

        self.driver = webdriver.Chrome(
            executable_path=chrome_path, options=options)

    def login(self):
        self.driver.set_window_position(0, 0)  # 瀏覽器位置
        self.driver.set_window_size(375, 900)  # 瀏覽器大小
        self.driver.implicitly_wait(10)  # seconds
        self.driver.get(
            # "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
            "http://h5.waimai.meituan.com/login")

        self.phone = self.config.get("option", "phone")
        phoneNumInput = self.driver.find_element_by_xpath(
            '//*[@id="phoneNumInput"]')
        phoneNumInput.send_keys(self.phone)
        self.verify_action()

    def get_track(self, distance):
        track = []
        current = 0
        mid = distance*3/5
        t = random.randint(2, 4)/10
        # t = 0.2
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
        return track

    def verify_action(self):
        try:
            iLoginCounDown = self.driver.find_element_by_xpath(
                '//*[@id="iLoginCounDown"]')
            time.sleep(1)
            r = requests.post('http://z-sms.com/admin/smslist.php', data = {'PhoNum':self.phone})
            sms = r.json()

            print(sms)
        except NoSuchElementException:
            print("No element found")

            sendCodeBtn = self.driver.find_element_by_xpath(
                '//*[@id="sendCodeBtn"]')
            sendCodeBtn.click()
            time.sleep(3)
            try:
                yodaBox = self.driver.find_element_by_xpath('//*[@id="yodaBox"]')
            except NoSuchElementException:
                self.verify_action()
            touch = TouchActions(self.driver)
            r = random.randint(1,2)
            if r == 1:
                tracks = self.get_track(270)
            else:
                offsets, tracks = easing.get_tracks(265, 10, 'easeInOutQuint')
                
            print(tracks)
            # offsets, tracks = easing.get_tracks(265, 10, 'easeInOutQuint')
            # print(tracks)
            # print(offsets)
            loc = yodaBox.location
            x = loc['x']+10
            y1 = loc['y']+10
            y2 = y1 +3
            y3 = y1 +6
            touch.tap_and_hold(x, y1)
            y_d = []
            # for track in track_list:
            #     x += track
            #     tmp = y + random.randint(-2,3) 
            #     touch.move(x+track, tmp)
            for i,track in enumerate(tracks):
                x += track
                if i/len(tracks) < 1/5 or i/len(tracks) > 4/5:
                    y = y1
                elif 2/5 <= i/len(tracks) <= 3/5:
                    y = y3
                else:
                    y = y2 
                y_d.append(y)
                touch.move(x, y)
            touch.release(x, y).perform()
            print(y_d)
            self.verify_action()


if __name__ == '__main__':
    SeleniumSpider().login()
