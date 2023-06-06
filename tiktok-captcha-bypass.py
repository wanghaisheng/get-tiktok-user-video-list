import os
import cv2
import time
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from natsort import natsorted
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions, ActionChains, DesiredCapabilities


chrome_options = ChromeOptions()
chrome_options.add_argument(f'user-agent={UserAgent().random}')
chrome_options.add_experimental_option('w3c', False)
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-dev-shm-usage')

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}


def url_to_img(url, save_as=False):
    img = Image.open(BytesIO(requests.get(url).content))
    if save_as:
        img.save(save_as)
    return np.array(img)


def image_to_video(image_files, video_name, fps):
    image_files = [cv2.imread(img) for img in image_files]
    height, width, layers = image_files[0].shape
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for img in image_files:
        video.write(img)

    cv2.destroyAllWindows()
    video.release()


class GSC_solver:

    def __init__(self, chrome_driver_path = 'chromedriver'):
        try:
            self.driver = webdriver.Chrome(chrome_driver_path,
                                        desired_capabilities=caps,
                                        options=chrome_options)
        except:
            self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                        desired_capabilities=caps,
                                        options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        self.path = None

    # -----------------------------------------------------------------------------

    def create_snapshot_dir(self, snapshot_path):
        self.path = f'{snapshot_path}/snapshot/{self.driver.session_id}'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.count = 0

    # -----------------------------------------------------------------------------

    def snapshot(self, obj=None):
        if self.path is not None:
            filename = f'{self.path}/{self.count}.png'
            if type(obj) == str or type(obj) == np.ndarray:
                try:
                    img = Image.open(BytesIO(requests.get(obj).content))
                except:
                    img = Image.fromarray(obj)
                finally:
                    if self.count > 1:
                        img.resize((340, 212), Image.ANTIALIAS)
                    img.save(filename)
            else:
                self.driver.save_screenshot(filename)
            self.count += 1

    # -----------------------------------------------------------------------------

    def get_dist(self, back_url):
        img = url_to_img(back_url)
        self.snapshot(back_url)

        card_img = cv2.resize(img, (340, 212), interpolation=cv2.INTER_NEAREST)
        self.snapshot(card_img)

        max_area = 1
        min_area = 0.5
        image = card_img
        # print(image.shape)
        result = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        self.snapshot(image)

        lower = np.array([0, 0, 240])  # TUNE
        upper = np.array([255, 255, 255])  # TUNE
        mask = cv2.inRange(image, lower, upper)
        self.snapshot(mask)

        #result = cv2.bitwise_and(result, result, mask=mask)
        edges = cv2.Canny(mask, 30, 200)  # TUNE
        self.snapshot(edges)

        contours, hierarchy = cv2.findContours(edges,
                                               cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        e2 = []
        for contour in contours:
            if contour.size > 100:  # TUNE
                e2.append(contour)
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.drawContours(card_img, e2, -1, (0, 255, 0), 3)
        self.snapshot(card_img)

        img2 = image
        total_x = []
        total_y = []
        total_n = 0
        for cnt in e2:
            approx = cv2.approxPolyDP(
                cnt, 0.009 * cv2.arcLength(cnt, True), True)
            # self.snapshot(approx)

            n = approx.ravel()
            i = 0
            for j in n:
                if(i % 2 == 0):
                    x = n[i]
                    y = n[i + 1]
                    total_x.append(x)
                    total_y.append(y)
                    total_n += 1
                i = i + 1
        cords = (min(total_x), (min(total_y)+max(total_y))//2)
        # print(cords)
        mid_point = cv2.circle(card_img, cords, radius=0,
                               color=(0, 0, 255), thickness=5)
        self.snapshot(mid_point)

        return min(total_x) - 4

    # -----------------------------------------------------------------------------

    def get_track(self, distance):
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

    # -----------------------------------------------------------------------------

    def move_slider(self, slider, track):
        self.snapshot()
        ActionChains(self.driver).click_and_hold(slider).perform()

        for x in track:
            ActionChains(self.driver).move_by_offset(
                xoffset=x, yoffset=0).perform()
            self.snapshot()

        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

        for _ in range(4):
            self.snapshot()

    # -----------------------------------------------------------------------------

    def export_video(self, path):
        image_files = natsorted(
            [path+'/'+img for img in os.listdir(path) if img.endswith(".png")])

        image_to_video(image_files[2:8], f'{path}/process.mp4', 1)
        image_to_video(image_files[8:], f'{path}/captcha.mp4', 24)

        [os.remove(img) for img in image_files]

    # -----------------------------------------------------------------------------

    def solve(self, var, snapshot_path=None):

        if snapshot_path is not None:
            self.create_snapshot_dir(snapshot_path)

        if type(var) == str:
            self.driver.get(var)
        elif type(var) == webdriver.chrome.webdriver.WebDriver:
            self.driver = var

        try:

            self.piece_url = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "img[class^='captcha_verify_img_slide react-draggabl']"))).get_attribute('src')
            self.snapshot(self.piece_url)

            self.back_url = self.wait.until(EC.element_to_be_clickable(
                (By.ID, "captcha-verify-image"))).get_attribute('src')
            print('Back URL has been fetched')

            slider = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[class^='secsdk-captcha-drag-icon']")))
            print('Slider has been detected')

            distance = self.get_dist(self.back_url)
            print('Distance has been calculated')

            track = self.get_track(distance)
            print('Track has been planned')

            self.move_slider(slider, track)
            print('Captcha has been solved')

            if snapshot_path is not None:
                self.export_video(self.path)

        except Exception as ex:
            print(ex)

        finally:
            return self.driver
