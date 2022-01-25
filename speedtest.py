from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import configparser
import apprise
import time

config = configparser.ConfigParser()
config.readfp(open(r'config/config.cfg'))

MIN_UPLOAD = config.get('Measurement', 'min-upload')
MIN_DOWNLOAD = config.get('Measurement', 'min-download')
TELEGRAM_TOKEN = config.get('Telegram', 'token')
TELEGRAM_ID = config.get('Telegram', 'ID')
MAILUSER = config.get('MAIL', 'username')
MAILDOMAIN = config.get('MAIL', 'maildomain')
MAILPASSWORD = config.get('MAIL', 'password')
MAILTO = config.get('MAIL', 'mailto')
TWITTERCKey = config.get('Twitter', 'consumerkey')
TWITTERCSecret = config.get('Twitter', 'consumersecret')
TWITTERAKey = config.get('Twitter', 'accesstoken')
TWITTERASecret = config.get('Twitter', 'accesssecret')
TEST_URL = "https://breitbandmessung.de/test"
FIREFOX_PATH = "firefox"
DOWNLOADED_PATH = "/export/"
SLEEPTIME = 10
SCREENSHOTNAME = "Breitbandmessung_"
SCREENSHOOTEXT = ".png"


#Buttons to click
allow_necessary = '#allow-necessary'
start_test_button = 'button.btn:nth-child(4)'
allow = 'button.btn:nth-child(2)'
website_header = '#root > div > div > div > div > div:nth-child(1) > h1'
download_result = 'button.px-0:nth-child(1)'
ping = 'div.col-md-6:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)'
ping_unit = 'div.col-md-6:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > span:nth-child(1)'
download = 'div.col-md-6:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)'
download_unit = 'div.col-md-6:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > span:nth-child(1)'
upload = '.col-md-12 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)'
upload_unit = '.col-md-12 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > span:nth-child(1)'


#Open browser an testpage breitbandmessung.de/test
print("Open Browser")
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
fireFoxOptions.set_preference("browser.download.folderList", 2)
fireFoxOptions.set_preference("browser.download.manager.showWhenStarting",False)
fireFoxOptions.set_preference("browser.download.dir", DOWNLOADED_PATH)
fireFoxOptions.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/force-download")
fireFoxOptions.set_preference("browser.download.panel.shown", False)
browser = webdriver.Firefox(options=fireFoxOptions)

browser.get("https://breitbandmessung.de/test")
print("Click all buttons")
accept_necessary_cookies = browser.find_element(By.CSS_SELECTOR, allow_necessary)
try:
    elem = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, allow_necessary))
    )
finally:
    browser.find_element(By.CSS_SELECTOR, allow_necessary)
accept_necessary_cookies = browser.find_element(By.CSS_SELECTOR, allow_necessary)
accept_necessary_cookies.click()

print("Wait until the location window disaper")
time.sleep(SLEEPTIME)
try:
    elem = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, start_test_button))
    )
finally:
    browser.find_element(By.CSS_SELECTOR, start_test_button)
print("Clicking the last buttons")
start_test_button = browser.find_element(By.CSS_SELECTOR, start_test_button)
start_test_button.click()

data_guidlines = browser.find_element(By.CSS_SELECTOR, allow)
data_guidlines.click()

print("Start messurment")
while True:
    try:
        header = browser.find_element_by_css_selector(website_header)
        if header.text == "Die Browsermessung ist abgeschlossen.":
            save_result = browser.find_element(By.CSS_SELECTOR, download_result)
            save_result.click()
            result_down = browser.find_element(By.CSS_SELECTOR, download)
            result_down_unit = browser.find_element(By.CSS_SELECTOR, download_unit)
            result_up = browser.find_element(By.CSS_SELECTOR, upload)
            result_up_unit = browser.find_element(By.CSS_SELECTOR, upload_unit)
            result_ping = browser.find_element(By.CSS_SELECTOR, ping)
            result_ping_unit = browser.find_element(By.CSS_SELECTOR, ping_unit)
            print("")
            print("Ping: ", result_ping.text, result_ping_unit.text)
            print("Download: ", result_down.text, result_down_unit.text)
            print("Upload: ", result_up.text,  result_up_unit.text)
            now = datetime.now()
            current_time = now.strftime("%H_%M_%S")
            current_date = now.strftime("%d_%m_%Y")
            filename = SCREENSHOTNAME + current_date + "_" + current_time + SCREENSHOOTEXT
            browser.save_screenshot(filename)
            break
    finally:
        time.sleep(SLEEPTIME)

if result_up.text >= MIN_UPLOAD and result_down.text >= MIN_DOWNLOAD:
    internet_to_slow = False
    print('Internet ok')
else:
    internet_to_slow = True

if internet_to_slow:
    print("Internet to slow")
    my_message = "Current Download is: " + result_down.text + " " + result_down_unit.text + " and current upload: " + result_up.text + " " + result_up_unit.text
    apobj = apprise.Apprise()
    config = apprise.AppriseConfig()
    #TelegramNOTIFY = 'tgram://' + TELEGRAM_TOKEN + '/' + TELEGRAM_ID
    #MAILNOTIFY = 'mailto://' + MAILUSER + ':' + MAILPASSWORD + '@' + MAILDOMAIN + '?to=' + MAILTO + '?from=' + MAILUSER + '&name=Breitbandmessung Docker'
    #TWITTERNOTIFY = 'twitter://' + TWITTERCKey + '/' + TWITTERCSecret + '/' + TWITTERAKey + '/'+ TWITTERASecret + '?mode=tweet'
    apobj.add('tgram://' + TELEGRAM_TOKEN + '/' + TELEGRAM_ID)
    apobj.add('mailto://' + MAILUSER + ':' + MAILPASSWORD + '@' + MAILDOMAIN + '?to=' + MAILTO + '?from=' + MAILUSER + '&name=Breitbandmessung Docker')
    apobj.add('twitter://' + TWITTERCKey + '/' + TWITTERCSecret + '/' + TWITTERAKey + '/'+ TWITTERASecret + '?mode=tweet')

    apobj.notify(
    body=my_message,
    title='Breitbandmessung.de Ergebnis',
    attach=filename,
    )

browser.close()
exit()
