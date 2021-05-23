from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import calender
import os

calender = calender.Calender()
calender.GetNameDict()

if len(calender.NameDict)<=0:
    import sys
    sys.exit(0)

else:
    for key,value in calender.NameDict.items():
        PROFILE = os.environ.get('PROFILE_PATH')

        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

        Options = webdriver.ChromeOptions()
        Options.add_argument('--user-data-dir={}'.format(PROFILE))
        Options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
        Options.headless = True
        Options.add_argument(f'user-agent={user_agent}')
        Options.add_argument("--window-size=1920,1080")
        Options.add_argument('--ignore-certificate-errors')
        Options.add_argument('--allow-running-insecure-content')
        Options.add_argument("--disable-extensions")
        Options.add_argument("--proxy-server='direct://'")
        Options.add_argument("--proxy-bypass-list=*")
        Options.add_argument("--start-maximized")
        Options.add_argument('--disable-gpu')
        Options.add_argument('--disable-dev-shm-usage')
        Options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), options=Options)
        driver.get('https://web.whatsapp.com/')
        
        driver.implicitly_wait(30)
        explicit_wait = WebDriverWait(driver,15)
        
        explicit_wait.until(ec.presence_of_element_located((By.XPATH,'//*[@id="side"]/div[1]/div/label/div/div[2]')))
        search_bar = driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
        search_bar.click()
        search_bar.send_keys(key)

        time.sleep(5)

        explicit_wait.until(ec.element_to_be_clickable(
            (By.XPATH,'//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div'))).click()
        time.sleep(2)

        explicit_wait.until(ec.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]')))
        message_bar = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]')
        message_bar.click()
        message_bar.send_keys(calender.NameDict[key])

        explicit_wait.until(ec.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div[3]')))
        send = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]')
        send.click()

    time.sleep(3)
    driver.quit()
