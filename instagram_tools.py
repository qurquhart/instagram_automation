import os
import pickle
from datetime import datetime
import json
# insta_post() - selenium/time/autoit
import time
import autoit
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# from this project
from mountain_project_tools import route_info_by_id


def insta_post(ig_username, ig_password, filepath, post_description, path_to_chromedriver):
    '''post to instagram using selenium/chrome'''

    def loading_time():
        '''wait for the page to load'''
        time.sleep(2)

    # set chrome settings to emulate mobile device
    mobile_emulation = {
        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D)"
        " AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option(
        "mobileEmulation", mobile_emulation)
    
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(
        path_to_chromedriver, chrome_options=chrome_options)

    # navigate to login page and input credentials
    driver.get('https://www.instagram.com/accounts/login/')

    loading_time()

    driver.find_element_by_name("username").send_keys(ig_username)
    driver.find_element_by_name("password").send_keys(ig_password)

    # login button
    driver.find_element_by_xpath(
        """//*[@id="react-root"]/section/main/article/div/div/div/form/div[7]/button""").click()

    loading_time()

    # go to profile page
    driver.get('https://www.instagram.com/' + ig_username)

    # init new post
    ActionChains(driver).move_to_element(driver.find_element_by_xpath(
        """//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]""")).click().perform()

    # set filelocation for image upload and open
    handle = "[CLASS:#32770; TITLE:Open]"
    autoit.win_wait(handle, 3)
    autoit.control_set_text(handle, "Edit1", filepath)
    autoit.control_click(handle, "Button1")

    # logging
    print(f"Uploading {filepath}")

    loading_time()

    # continue to description options
    driver.find_element_by_xpath(
        """//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()

    loading_time()

    # set description and submit post
    txt = driver.find_element_by_class_name('_472V_')
    txt.send_keys('')
    txt = driver.find_element_by_class_name('_472V_')
    txt.send_keys(post_description)  # Descrition
    txt.send_keys(Keys.ENTER)

    loading_time()
    loading_time()

    # submit button
    driver.find_element_by_xpath(
        """//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()

    loading_time()
    loading_time()
    loading_time()
    loading_time()
    loading_time()
    loading_time()

    driver.quit()


def mountain_project_poster(ig_username, ig_password, hashtags, path_to_chromedriver):
    '''looks through stored route data, finds unposted route image,
    posts to instagram, and adds route_id to logfile'''

    f = open('post_log.txt', 'a+')
    f.write(
        f'{datetime.now()} - [{ig_username}] Initiated mountain project poster.\r\n')
    f.close()

    route_history = []
    # expand error reporting for unfound items?
    if os.path.isfile("data/post_history.p"):
        route_history = pickle.load(open("data/post_history.p", "rb"))

    # load route info
    route_info = json.load(open('data/route_info.json', 'r'))

    skipped_routes = 0

    posted = 0

    print(f'pre ifelse - posted = {posted}')
    for route in route_info["routes"]:
        # clean this up
        route_id = route["id"]
        if posted == 0:
            if route_id not in route_history:

                images_not_found = 0
                
                if not os.path.isfile(f"images/{route_id}.jpg"):
                    images_not_found += 1

                else:

                    print(f'before post stage - posted = {posted}')
                    # upload to instagram and add id to route history
                    try:

                        image = os.path.abspath(f'images/{route_id}.jpg')
                        instagram_caption = f'{route_info_by_id(route_id)}' + \
                            '\r\n\r\n\r\n' + hashtags
                        insta_post(ig_username, ig_password,
                                image, instagram_caption, path_to_chromedriver)
                        print('!!!!!!!!!! ITEM HAS POSTED !!!!!!!!!!!!')
                        route_history.append(route_id)
                        f = open('post_log.txt', 'a+')
                        f.write(f'{datetime.now()} - [{ig_username}] Posted route ID: {route_id}\r\n')
                        f.close()
                        posted = 1

                    except Exception as ex:
                        f = open('post_log.txt', 'a+')
                        f.write(
                            f'{datetime.now()} - ERROR! UNABLE TO POST ROUTE ID {route_id}: {ex}\r\n')
                        f.close()
                        continue

                    # save post history
                    pickle.dump(route_history, open(
                        "data/post_history.p", "wb"))

            else:
                skipped_routes += 1

    if images_not_found != 0:
        print(f'{images_not_found} attempted image files were not found.')

    f = open('post_log.txt', 'a+')
    f.write(f'{datetime.now()} - [{ig_username}] Routes in post history: {skipped_routes}'
            f' - Attempted posts on routes with unavailable images: {images_not_found}\r\n')
    f.close()
    print(f'Routes in post history: {skipped_routes}'
          f' - Attempted posts on routes with unavailable images: {images_not_found}')


def remove_from_history(route_id):
    route_history = pickle.load(open("data/post_history.p", "rb"))
    route_history.remove(route_id)
    pickle.dump(route_history, open("data/post_history.p", "wb"))
    print(f"[Post History] Removed route ID: {route_id}")


def add_to_history(route_id):
    route_history = pickle.load(open("data/post_history.p", "rb"))
    route_history.append(route_id)
    pickle.dump(route_history, open("data/post_history.p", "wb"))
    print(f"[Post History] Added route ID: {route_id}")