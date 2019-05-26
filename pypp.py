import asyncio
from pyppeteer import launch
import random
import time

async def main():
    browser = await launch({
        'executablePath': 'D:\learning\meituan_spider\chrome-win\chrome.exe',
        'headless': False, 
        'args': ['--no-sandbox']
    })
    page = await browser.newPage()
    await page.emulate({
        'name': 'iPhone 7 Plus',
        'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'viewport': {
            'width': 414,
            'height': 736,
            'deviceScaleFactor': 3,
            'isMobile': True,
            'hasTouch': True,
            'isLandscape': False
        }
    })
    await page.setViewport({'width': 414, 'height': 736})
    # await page.setUserAgent(
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
    await page.goto('https://h5.waimai.meituan.com/login')
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    
    wait = page.waitForSelector('#phoneNumInput')
    print(wait)
    await wait
    await page.waitFor(2000)
    await page.type('#phoneNumInput','16734065668',{'delay': random.randint(90, 131)})
    time.sleep(100000)

    await page.waitForSelector('#sendCodeBtn')
    await page.click("#sendCodeBtn")

    time.sleep(100000)

asyncio.get_event_loop().run_until_complete(main())