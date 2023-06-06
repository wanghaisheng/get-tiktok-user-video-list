from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, WebDriverException

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import platform
import requests
import time
from .util import get_undetected_webdriver
import undetected_chromedriver as uc
import os
import cv2 as cv
import numpy as np


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
def scroll_to_bottom_of_page_comment(web_driver):

    SCROLL_PAUSE_TIME = 2
    CYCLES = 7
    html = web_driver.find_element_by_tag_name('html')
    html.send_keys(Keys.PAGE_DOWN)   
    html.send_keys(Keys.PAGE_DOWN)   
    time.sleep(SCROLL_PAUSE_TIME * 3)
    for i in range(CYCLES):
        html.send_keys(Keys.END)
        time.sleep(SCROLL_PAUSE_TIME)
def scroll_infi(driver,SCROLL_PAUSE_TIME):
    if SCROLL_PAUSE_TIME =='':
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

def get_track(distance):
    track = []
    current = 0
    mid = distance * 4 / 5
    t = 0.2
    v = 0

    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track
def move_slider(web_driver, slider, track):
    ActionChains(web_driver).click_and_hold(slider).perform()

    for x in track:
        ActionChains(web_driver).move_by_offset(
            xoffset=x, yoffset=0).perform()

    time.sleep(0.5)
    ActionChains(web_driver).release().perform()

def get_user_video_count_douyin_undetected(url):
    print('====initiliaze webdriver=====')

    # web_driver = getwebdriver_chrome()
    # print('url getting',web_driver.title(url),web_driver.get(url))
    # out = web_driver.get(url)
    web_driver=get_undetected_webdriver(False)

    out =web_driver.get(url)        
    wait = WebDriverWait(web_driver, 1)
    try:
        web_driver.find_element(By.CSS_SELECTOR, "img[class^='captcha_verify_img_slide']")

        piece_url = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "img[class^='captcha_verify_img_slide react-draggabl']"))).get_attribute('src')
        code_path = "./image/code.png"  # 验证码背景图
        if not os.path.exists("./image"):
            os.makedirs("./image")           
        web_driver.save_screenshot(code_path)

        back_url = wait.until(EC.element_to_be_clickable(
            (By.ID, "captcha-verify-image"))).get_attribute('src')
        print('Back URL has been fetched')

        slider = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div[class^='secsdk-captcha-drag-icon']")))
        print('Slider has been detected')
        img = cv.imread(code_path)
        card_img=img            
        img_blur = cv.GaussianBlur(card_img, (7, 7), 1)
        img = cv.medianBlur(img,5)
        img_gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)
        ret2,thresh = cv.threshold(img_gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        img_canny = cv.Canny(thresh, 50, 190)
        
        kernel = np.ones((3))
        # erosion = cv.erode(img_canny, kernel, iterations=1)            
        img_dilated = cv.dilate(img_canny, kernel, iterations=1)
        # cv.imshow('img_dilated', img_dilated)
        # cv.waitKey(0)
        contours, hierarchy = cv.findContours(img_dilated,
                                                cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        e2 = []
        offsetlist = []
        # for contour in contours:

        for i,cnt in enumerate(contours):
                # if the contour has no other contours inside of it
            if hierarchy[0][i][2] == -1 :
                        # if the size of the contour is greater than a threshold
                # if  cv.contourArea(cnt) > 10000:
                x, y, w, h = cv.boundingRect(cnt)
                print(x,y,w,h)
                if cnt.size > 300 and w > 40 and h > 40 and x-slider['x'] > 60:  # TUNE
                    offsetlist.append(x)
                    e2.append(cnt)
        print(offsetlist,'======!')
        final =cv.drawContours(card_img, e2, -1, (0, 255, 0), 3)

        offsetlist=sorted(list(set(offsetlist)))
        for distance in offsetlist:
            print('Distance has been calculated')

            track = get_track(distance)
            print('Track has been planned')

            move_slider(slider, track)
            print('Captcha has been solved')
    except:
        print('no slide at all ')        
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.CANY1MjK.GKO_f9Vh > span")))
    # count = page.query_selector("#root > div > div.T_foQflM > div > div > div.ckqOrial > div.mwbaK9mv > div.isaIlRLR > div.CANY1MjK.GKO_f9Vh > span#root > div > div.T_foQflM > div > div > div.ckqOrial > div.mwbaK9mv > div.isaIlRLR > div.CANY1MjK.GKO_f9Vh > span").text_content()

    count=web_driver.find_elements(By.CSS_SELECTOR,"div.CANY1MjK:nth-child(1) > span:nth-child(1)")[0].text
    print('video count',count)
    return count

def get_user_video_list_douyin_undetected(url):
    print('====initiliaze webdriver=====')

    # web_driver = getwebdriver_chrome()
    # print('url getting',web_driver.title(url),web_driver.get(url))
    # out = web_driver.get(url)
    web_driver=get_undetected_webdriver(False)

    out =web_driver.get(url)        
    wait = WebDriverWait(web_driver, 1)
    try:
        web_driver.find_element(By.CSS_SELECTOR, "img[class^='captcha_verify_img_slide']")

        piece_url = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "img[class^='captcha_verify_img_slide react-draggabl']"))).get_attribute('src')
        code_path = "./image/code.png"  # 验证码背景图
        if not os.path.exists("./image"):
            os.makedirs("./image")           
        web_driver.save_screenshot(code_path)

        back_url = wait.until(EC.element_to_be_clickable(
            (By.ID, "captcha-verify-image"))).get_attribute('src')
        print('Back URL has been fetched')

        slider = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div[class^='secsdk-captcha-drag-icon']")))
        print('Slider has been detected')
        img = cv.imread(code_path)
        card_img=img            
        img_blur = cv.GaussianBlur(card_img, (7, 7), 1)
        img = cv.medianBlur(img,5)
        img_gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)
        ret2,thresh = cv.threshold(img_gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        img_canny = cv.Canny(thresh, 50, 190)
        
        kernel = np.ones((3))
        # erosion = cv.erode(img_canny, kernel, iterations=1)            
        img_dilated = cv.dilate(img_canny, kernel, iterations=1)
        # cv.imshow('img_dilated', img_dilated)
        # cv.waitKey(0)
        contours, hierarchy = cv.findContours(img_dilated,
                                                cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        e2 = []
        offsetlist = []
        # for contour in contours:

        for i,cnt in enumerate(contours):
                # if the contour has no other contours inside of it
            if hierarchy[0][i][2] == -1 :
                        # if the size of the contour is greater than a threshold
                # if  cv.contourArea(cnt) > 10000:
                x, y, w, h = cv.boundingRect(cnt)
                print(x,y,w,h)
                if cnt.size > 300 and w > 40 and h > 40 and x-slider['x'] > 60:  # TUNE
                    offsetlist.append(x)
                    e2.append(cnt)
        print(offsetlist,'======!')
        final =cv.drawContours(card_img, e2, -1, (0, 255, 0), 3)

        offsetlist=sorted(list(set(offsetlist)))
        for distance in offsetlist:
            print('Distance has been calculated')

            track = get_track(distance)
            print('Track has been planned')

            move_slider(slider, track)
            print('Captcha has been solved')
    except:
        print('no slide at all ')        
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.CANY1MjK.GKO_f9Vh > span")))
    # count = page.query_selector("#root > div > div.T_foQflM > div > div > div.ckqOrial > div.mwbaK9mv > div.isaIlRLR > div.CANY1MjK.GKO_f9Vh > span#root > div > div.T_foQflM > div > div > div.ckqOrial > div.mwbaK9mv > div.isaIlRLR > div.CANY1MjK.GKO_f9Vh > span").text_content()

    count=web_driver.find_elements(By.CSS_SELECTOR,"div.CANY1MjK:nth-child(1) > span:nth-child(1)")[0].text
    print('video count',count)
    # douyin 一屏只有16个视频
    if int(count)<16:
        pausetime=0.5
    else:
        pausetime=(int(count)/48+1)*0.5
        # scroll_to_bottom_of_page(web_driver,pausetime)
    scroll_infi(web_driver,pausetime)
    # print(len(video_ids_list))
    video_ids_list = [
    video_element.get_attribute("href") + "\n"
    # "//*[@class='ARNw21RN']/li"
    for video_element in web_driver.find_elements(by=By.XPATH, value= "//*[@class='ECMy_Zdt']/a") ]
    print(len(video_ids_list))
    if abs(int(count)-len(video_ids_list))>5:
        scroll_infi(web_driver,pausetime)

        video_ids_list = [
        video_element.get_attribute("href").split('/')[-1]
    # "//*[@class='ARNw21RN']/li"
    for video_element in web_driver.find_elements(by=By.XPATH, value= "//*[@class='ECMy_Zdt']/a") ]



    return video_ids_list
# url='https://www.douyin.com/user/MS4wLjABAAAAUpIowEL3ygUAahQB47vy8sbYMB1eIr40qtlDwxhxFGw'

# get_user_video_list_douyin_undetected(url)