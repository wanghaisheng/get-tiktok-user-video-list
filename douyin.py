from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, WebDriverException

from selenium import webdriver

def getwebdriver_chrome():
    chrome_options = Options()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_experimental_option('useAutomationExtension', False)

    prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
    if url_ok('www.google.com'):
        print('no proxy need at all')
    else:
        # chrome_options.add_argument("proxy-server=socks5://127.0.0.1:1080")
        print('need proxy for google')
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])

    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    print('debug',platform.system())
    if 'Windows' in platform.system():
        print('debug')
        EDGE_DRIVER_PATH='D:/Download/audio-visual/objection_engine/assets/driver/chromedriver.exe'
        service = ChromiumService(EDGE_DRIVER_PATH, start_error_message='error')

        web_driver = webdriver.ChromiumEdge(service=service, options=chrome_options)
        # web_driver = webdriver.Chrome(service=Service("D:\Download\audio-visual\tiktok\Douyin-DownloadAllVideo\chromedriver.exe"), options=chrome_options)
        web_driver.maximize_window()

        print('windows system chrome driver ',web_driver)

    else:
        web_driver = webdriver.Chrome(service=Service(r""), options=chrome_options)
        print('other system')
    

    return web_driver

def url_ok(url):


    try:
        response = requests.head(url)
    except Exception as e:
        # print(f"NOT OK: {str(e)}")
        return False
    else:
        if response.status_code == 200:
            # print("OK")
            return True
        else:
            print(f"NOT OK: HTTP response code {response.status_code}")

            return False   
def scroll_to_bottom_of_page(web_driver):
    time.sleep(5)

    get_scroll_height_command = (
        "return (document.documentElement || document.body).scrollHeight;"
    )
    scroll_to_command = "scrollTo(0, {});"

    # Set y origin and grab the initial scroll height
    y_position = 0
    scroll_height = web_driver.execute_script(get_scroll_height_command)

    
    # while True:
    #     if len(web_driver.find_elements_by_xpath("//*[@id='root']/div/div[2]/div/div/div[4]/div[1]/div[2]/ul/li/a/@href")) > 0:
    #         break
    #     web_driver.refresh()
        

    print("Opened url, scrolling to bottom of page...")
    # While the scrollbar can still scroll further down, keep scrolling
    # and asking for the scroll height to check again
    while y_position != scroll_height:
        y_position = scroll_height
        web_driver.execute_script(scroll_to_command.format(scroll_height))

        # Page needs to load yet again otherwise the scroll height matches the y position
        # and it breaks out of the loop
        time.sleep(5)
        scroll_height = web_driver.execute_script(get_scroll_height_command)

def get_video(url):
    try:
        print('====initiliaze webdriver=====')

        web_driver = getwebdriver_chrome()
        print('url getting')
        out = web_driver.get(url)
        print(out)
        scroll_to_bottom_of_page(web_driver)

        wait = WebDriverWait(web_driver, 10)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='root']/div/div[2]/div/div/div[2]")))
        while not web_driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/div/div[2]"):
            print('page not show')
            time.sleep(0.1)
            finished = web_driver.find_element_by_xpath(
                "//*[@id='root']/div/div[2]/div/div/div[2]")
            if finished == True:
                break
        video_urls = [div.attrs['data-asin'] for div in driver.find_all("//*[@id='root']/div/div[2]/div/div/div[4]/div[1]/div[2]/ul/li/a')") ]
        for video in video_urls:
            print(video)

    except:
        pass
