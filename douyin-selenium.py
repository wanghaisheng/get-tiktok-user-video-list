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
    if 'Windows' in platform.system():
        print('debug')
        EDGE_DRIVER_PATH='D:/Download/audio-visual/objection_engine/assets/driver/chromedriver.exe'
        # service = ChromiumService(EDGE_DRIVER_PATH, start_error_message='error')

        # web_driver = webdriver.ChromiumEdge(service=service, options=chrome_options)
        web_driver = webdriver.Chrome(executable_path=EDGE_DRIVER_PATH, chrome_options=chrome_options)
        # print('url getting',web_driver.get('baidu.com'))

        # web_driver.maximize_window()

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
def scroll_to_bottom_of_page(web_driver,pausetime):
    if pausetime is None:
        pausetime=5
    time.sleep(pausetime)

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
        time.sleep(pausetime)
        scroll_height = web_driver.execute_script(get_scroll_height_command)

def scroll_infi(driver):
    SCROLL_PAUSE_TIME = 0.5
    while True:

        # Get scroll height
        ### This is the difference. Moving this *inside* the loop
        ### means that it checks if scrollTo is still scrolling 
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")

            # check if the page height has remained the same
            if new_height == last_height:
                # if so, you are done
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue
def get_user_video_list_tiktok(url):
    # /html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[98]/div[1]/div/div
    pass
def get_user_video_list_douyin(url):
    try:
        print('====initiliaze webdriver=====')

        web_driver = getwebdriver_chrome()
        # print('url getting',web_driver.title(url),web_driver.get(url))
        out = web_driver.get(url)
        wait = WebDriverWait(web_driver, 10)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span")))
        count=web_driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span")[0].text
        print('video count',)
        # douyin 一屏只有16个视频
        if int(count)<16:
            pass
        else:
            pausetime=(int(count)/48+1)*0.5
        # scroll_to_bottom_of_page(web_driver,pausetime)
        scroll_infi(web_driver)
        video_ids_list = [
        video_element.get_attribute("href") + "\n"
        # "//*[@class='ARNw21RN']/li"
        for video_element in web_driver.find_elements_by_xpath(
            "//*[@class='ECMy_Zdt']/a"
        )]
        print(len(video_ids_list))
    except:
        pass
