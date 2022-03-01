
def getwebdriver_chrome():
    chrome_options = webdriver.ChromeOptions()
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
        pass
    else:
        chrome_options.add_argument("proxy-server=socks5://127.0.0.1:1080")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])

    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    if 'Windows' in platform.system():
        web_driver = webdriver.Chrome(executable_path="assets/driver/chromedriver.exe", chrome_options=chrome_options)
        # print('windows system chrome driver ',web_driver)

    else:
        web_driver = webdriver.Chrome(executable_path="assets/driver/chromedriver", chrome_options=chrome_options)
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
def scroll_until_loaded(self):
    check_height = self.browser.execute_script("return document.body.scrollHeight;")
    while True:
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            self.wait.until(lambda driver: self.browser.execute_script("return document.body.scrollHeight;")   check_height)
            check_height = self.browser.execute_script("return document.body.scrollHeight;")
        except TimeoutException:
            break
