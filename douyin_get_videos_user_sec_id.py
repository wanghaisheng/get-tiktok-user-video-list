import time
from .util import url_ok
from playwright.sync_api import sync_playwright,Mouse
import json
import requests
# from .util import *
def get_playright(playwright,url,headless:bool=True):
    #     browser = p.chromium.launch()
    #     browser = p.firefox.launch(headless=False)
    if headless=='':
        headless=True
    PROXY_SOCKS5 = "socks5://127.0.0.1:1080"
    browser=''
    if url_ok(url):
        try:
            browser = playwright.firefox.launch(headless=headless)
            print('start is ok')
        except:
            print('pl start failed')

    else: 
        browserLaunchOptionDict = {
        "headless": headless,
        "proxy": {
                "server": PROXY_SOCKS5,
        }
        } 
        browser = playwright.firefox.launch(**browserLaunchOptionDict)
        # Open new page    
    page = browser.new_page()
    res=page.goto(url)
    print(res,'====')
    return page,res

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
def scroll(page,pausetime):


    page.evaluate(
        """
        var intervalID = setInterval(function () {
            var scrollingElement = (document.scrollingElement || document.body);
            scrollingElement.scrollTop = scrollingElement.scrollHeight;
        }, 200);

        """
    )
    prev_height = None
    while True:
        curr_height = page.evaluate('(window.innerHeight + window.scrollY)')
        if not prev_height:
            prev_height = curr_height
            time.sleep(pausetime)
        elif prev_height == curr_height:
            page.evaluate('clearInterval(intervalID)')
            break
        else:
            prev_height = curr_height
            time.sleep(pausetime)
def validate_uidhome(url):
    with sync_playwright() as p:
        print('user home url',url)
        page,res = get_playright(p,url,True)
        # print(res.text())
        try:
            t=page.locator('div.CANY1MjK:nth-child(1) > span:nth-child(1)')
            # t.wait_for(timeout=10)
            
            if int(t.text_content())>0:
                return True
            else:
                return False
        except:
            try:
                t=page.locator('.P6wJrwQ6')
                # t.wait_for(timeout=10)

                if t.text_content()=='用户不存在':
                    return False
                else:
                    return True
            except:
                return False
def get_user_video_count_douyin_pl(url):
    with sync_playwright() as p:
        start = time.time()
        print('user home url',url)
        page,res = get_playright(p,url,True)
        # page = browser.new_page()
        # page.goto(url)
        # page.wait_for_selector("#root > div > div.T_foQflM > div > div > div.ckqOrial > div.mwbaK9mv > div.isaIlRLR > div.CANY1MjK.GKO_f9Vh > span", timeout=5000)  # 等待元素出现
        count = page.locator("div.CANY1MjK:nth-child(1) > span:nth-child(1)").text_content()
        print('video count',count)
    return int(count)
def get_user_video_list_douyin_pl(url,increment=0):
    with sync_playwright() as p:
        start = time.time()
        print('user home url',url)
        page,res = get_playright(p,url,True)
        # page = browser.new_page()
        # page.goto(url)
        # page.wait_for_selector("#root > div > div.T_foQflM > div > div > div.ckqOrial > div.mwbaK9mv > div.isaIlRLR > div.CANY1MjK.GKO_f9Vh > span", timeout=5000)  # 等待元素出现
        count = page.locator("div.CANY1MjK:nth-child(1) > span:nth-child(1)").text_content()
        print('video count',count)
        # query db for existing count
        
        # douyin 一屏只有16个视频
        if int(count)<16:
            pausetime=0
        else:
            pausetime=((int(count)/48)+1)*0.5
        if increment:
            scrolltimes=int(int(increment)/16)
            if scrolltimes==0:
                pass
            else:
                for i in range(0,scrolltimes):
                    page.mouse.wheel(0,page.viewport_size['height'])
                    page.evaluate("for (let i = 0; i < document.body.scrollHeight; i += 100) { window.scrollTo(0, i);}" )
                    time.sleep(pausetime*0.3)
                    page.locator('#root > div > div.T_foQflM > div > footer > div > div.uy0xcb2o > div:nth-child(6)').scroll_into_view_if_needed()
        else:
            scroll(page,pausetime)
        # scroll_to_bottom_of_page('',page,pausetime)

        video_ids_list = [
        video_element.get_attribute("href").split('/')[-1]
        # "//*[@class='ARNw21RN']/li"
        for video_element in page.query_selector_all(
            "//*[@class='ECMy_Zdt']/a"
        )]
        print(len(video_ids_list))
        if abs(int(count)-len(video_ids_list))>5:
            scroll(page,pausetime)
            video_ids_list = [
        video_element.get_attribute("href").split('/')[-1]
        # "//*[@class='ARNw21RN']/li"
        for video_element in page.query_selector_all(
            "//*[@class='ECMy_Zdt']/a"
        )]
        end = time.time()
        print('%.4f秒' % (end - start))
    return video_ids_list,int(count)

headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
        }


# get_user_video_list_douyin(url)
# url='https://www.douyin.com/user/MS4wLjABAAAAUpIowEL3ygUAahQB47vy8sbYMB1eIr40qtlDwxhxFGw'
# print(get_user_video_list_douyin_pl(url))

