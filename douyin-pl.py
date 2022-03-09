
# from .util import *
def get_playright(playwright,url,headless:bool=True):
    #     browser = p.chromium.launch()
    #     browser = p.firefox.launch(headless=False)

    PROXY_SOCKS5 = "socks5://127.0.0.1:1080"

    browserLaunchOptionDict = {
        "headless": headless,
        "proxy": {
                "server": PROXY_SOCKS5,
        }
        }
    if 'douyin' in url:
        browser = playwright.chromium.launch(headless=headless)

    else:
        browser = playwright.chromium.launch(**browserLaunchOptionDict)
#     context = browser.new_context(proxy={"server": "socks5://127.0.0.1:1080"})
        # Open new page    
    page = browser.new_page()
    page.goto(url)
    return page

def scroll_to_bottom_of_page(web_driver,page,pausetime):
    if pausetime is None:
        pausetime=0.05

    get_scroll_height_command = (
        "return (document.documentElement || document.body).scrollHeight;"
    )
    scroll_to_command = "scrollTo(0, {});"
    
    # Set y origin and grab the initial scroll height
    y_position = 0
    if web_driver and not web_driver=='':
        scroll_height = web_driver.execute_script(get_scroll_height_command)
    else:
        # pass
        scroll_height=  page.evaluate(" (document.documentElement || document.body).scrollHeight")

    print("Opened url, scrolling to bottom of page...")
    # While the scrollbar can still scroll further down, keep scrolling
    # and asking for the scroll height to check again
    while y_position != scroll_height:
        y_position = scroll_height
        if web_driver and not web_driver=='':
            web_driver.execute_script(scroll_to_command.format(scroll_height))
        else:
            page.mouse.wheel(0,scroll_height)

        # Page needs to load yet again otherwise the scroll height matches the y position
        # and it breaks out of the loop
        time.sleep(pausetime)
        if web_driver and not web_driver=='':
            scroll_height = web_driver.execute_script(get_scroll_height_command)
        else:
            scroll_height=  page.evaluate(" (document.documentElement || document.body).scrollHeight")
    # isend  = page.evaluate("async () => { \
    #     let scrollPosition = 0 \
    #     let documentHeight = document.body.scrollHeight \
    #     while (documentHeight > scrollPosition) { \
    #         window.scrollBy(0, documentHeight) \
    #         await new Promise(resolve => { \
    #         setTimeout(resolve, 1000) \
    #         }) \
    #         scrollPosition = documentHeight \
    #         documentHeight = document.body.scrollHeight        }) \
    #     }")
    # print('isend,',isend)
def get_user_video_list_tiktok_pl(url):
    # /html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[98]/div[1]/div/div
    pass
def get_user_video_list_douyin_pl(url,page):
    with sync_playwright() as p:

        page = get_playright(p,url)
        # page = browser.new_page()
        page.goto(url)
        page.wait_for_selector("#root > div > div.T_foQflM > div > div > div.ckqOrial > div.mwbaK9mv > div.isaIlRLR > div.CANY1MjK.GKO_f9Vh > span", timeout=5000)  # 等待元素出现
        count = page.query_selector("#root > div > div.T_foQflM > div > div > div.ckqOrial > div.mwbaK9mv > div.isaIlRLR > div.CANY1MjK.GKO_f9Vh > span").text_content()
        print('video count',count)
        # douyin 一屏只有16个视频
        if int(count)<16:
            pass
        else:
            pausetime=(int(count)/48+1)*0.5
        scroll_to_bottom_of_page('',page,pausetime)

        video_ids_list = [
        video_element.get_attribute("href") + "\n"
        # "//*[@class='ARNw21RN']/li"
        for video_element in page.query_selector_all(
            "//*[@class='ECMy_Zdt']/a"
        )]
        print(len(video_ids_list))

    return video_ids_list


def get_user_video_list_douyin_selenium(url,web_driver):

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
    scroll_to_bottom_of_page(web_driver,pausetime)
    # scroll_infi(web_driver)
    video_ids_list = [
    video_element.get_attribute("href") + "\n"
    # "//*[@class='ARNw21RN']/li"
    for video_element in web_driver.find_elements_by_xpath(
        "//*[@class='ECMy_Zdt']/a"
    )]
    print(len(video_ids_list))
    return video_ids_list
