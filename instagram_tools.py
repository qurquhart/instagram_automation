import os
import pickle
# insta_post() - selenium/time/autoit
import time
import autoit
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# from this project
from mountain_project_tools import route_info_by_id, load_route_info
from logger import Logger


def insta_post(ig_username, ig_password, image_filepath, ig_caption, path_to_chromedriver):
    '''post to instagram using selenium/chrome'''

    log = Logger('activity_log.txt', f'insta_post] [{ig_username}')

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

    driver = webdriver.Chrome(
        path_to_chromedriver, chrome_options=chrome_options)

    # navigate to login page and input credentials
    driver.get('https://www.instagram.com/accounts/login/')

    log.text('Initialized chromedriver.')

    loading_time()

    driver.find_element_by_name("username").send_keys(ig_username)
    driver.find_element_by_name("password").send_keys(ig_password)

    # login button
    driver.find_element_by_xpath(
        """//*[@id="react-root"]/section/main/article/div/div/div/form/div[7]/button""").click()

    loading_time()

    # go to profile page
    driver.get('https://www.instagram.com/' + ig_username)

    log.text('Logged in and navigated to profile page.')

    # init new post
    ActionChains(driver).move_to_element(driver.find_element_by_xpath(
        """//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]""")).click().perform()

    # set filelocation for image upload and open
    handle = "[CLASS:#32770; TITLE:Open]"
    autoit.win_wait(handle, 3)
    autoit.control_set_text(handle, "Edit1", image_filepath)
    autoit.control_click(handle, "Button1")

    # logging
    log.text('Uploaded image to instagram.')

    loading_time()

    # continue to description options
    driver.find_element_by_xpath(
        """//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()

    loading_time()

    # set description and submit post
    txt = driver.find_element_by_class_name('_472V_')
    txt.send_keys('')
    txt = driver.find_element_by_class_name('_472V_')
    txt.send_keys(ig_caption)  # Descrition
    txt.send_keys(Keys.ENTER)

    loading_time()
    loading_time()

    # submit button
    driver.find_element_by_xpath(
        """//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()

    log.text('Posted image to instagram.')

    loading_time()
    loading_time()
    loading_time()
    loading_time()
    loading_time()
    loading_time()

    driver.quit()

    log.text('Quit chromedriver.')


def mountain_project_poster(ig_username, ig_password, hashtags, path_to_chromedriver):
    '''looks through stored route data, finds unposted route image,
    posts to instagram, and adds route_id to logfile'''

    log = Logger('activity_log.txt',
                 f'mountain_project_poster] [{ig_username}')
    error = Logger('error_log.txt',
                   f'mountain_project_poster] [{ig_username}')

    log.text('Initialized mountain project poster.')

    route_history = []
    # expand error reporting for unfound items?
    if os.path.isfile("data/post_history.p"):
        route_history = pickle.load(open("data/post_history.p", "rb"))
        log.text('Loaded post history.')
    else:
        log.text('Post history not found, continuing with empty history.')

    # load route info
    route_info = False

    route_info = load_route_info()

    skipped_routes = 0

    posted = 0

    if route_info is False:
        error.text('Route info not found')
    else:
        for route in route_info["routes"]:
            route_id = route["id"]
            if not posted == 0:
                break
            else:
                if route_id not in route_history:

                    images_not_found = 0

                    if not os.path.isfile(f"images/{route_id}.jpg"):
                        images_not_found += 1

                    else:
                        # upload to instagram and add id to route history
                        try:

                            image = os.path.abspath(f'images/{route_id}.jpg')
                            instagram_caption = f'{route_info_by_id(route_id)}' + \
                                '\r\n\r\n\r\n' + hashtags

                            log.text(
                                f'Attempting to post route ID: {route_id}')

                            insta_post(ig_username, ig_password,
                                       image, instagram_caption, path_to_chromedriver)

                            route_history.append(route_id)

                            log.text(
                                f'Adding route to history, route ID: {route_id}')

                            posted = 1

                        except Exception as ex:
                            error.text(
                                f'Unable to post route ID {route_id}: {ex}')
                            continue

                        # save post history pickle

                        def write_route_history(route_history_list):
                            pickle.dump(route_history_list, open(
                                "data/post_history.p", "wb+"))
                            log.text('Route history saved to disk.')

                        # check for directory and save
                        if os.path.isdir('data/'):
                            write_route_history(route_history)
                        else:
                            # create directory
                            os.makedirs(os.path.dirname(
                                'data/'), exist_ok=True)
                            log.text('Data directory not found, creating now.')
                            write_route_history(route_history)

                else:
                    # for logging how many routes in history
                    skipped_routes += 1

    if images_not_found != 0:
        log.text(f'{images_not_found} attempted image files were not found.')

    log.text(f'Routes in post history: {skipped_routes}')
    log.text(f'Attempted posts on routes with unavailable images: {images_not_found}')


def remove_from_history(route_id):
    log = Logger('activity_log.txt','remove_from_history')
    error = Logger('error_log.txt', 'remove_from_history')

    # open file and remove route id from list
    route_history = pickle.load(open("data/post_history.p", "rb"))
    route_history.remove(route_id)
    log.text(f"Removed route ID: {route_id}")

    def write_route_history(route_history_list):
        pickle.dump(route_history_list, open("data/post_history.p", "wb+"))
        log.text('Route history saved to disk.')

    try:
        # check for directory and save
        if os.path.isdir('data/'):
            write_route_history(route_history)
        else:
            # create directory
            os.makedirs(os.path.dirname('data/'), exist_ok=True)
            log.text('Data directory not found, creating now.')
            write_route_history(route_history)
    except Exception as ex:
        error.text(f'Failed to save route history: {ex}')


def add_to_history(route_id):
    log = Logger('activity_log.txt','add_to_history')
    error = Logger('error_log.txt', 'add_to_history')

    route_history = pickle.load(open("data/post_history.p", "rb"))
    route_history.append(route_id)
    log.text(f"Added route ID: {route_id}")

    def write_route_history(route_history_list):
        pickle.dump(route_history_list, open("data/post_history.p", "wb+"))
        log.text('Route history saved to disk.')

    try:
        # check for directory and save
        if os.path.isdir('data/'):
            write_route_history(route_history)
        else:
            # create directory
            os.makedirs(os.path.dirname('data/'), exist_ok=True)
            log.text('Data directory not found, creating now.')
            write_route_history(route_history)
    except Exception as ex:
        error.text(f'Failed to save route history: {ex}')


def reset_post_history():
    log = Logger('activity_log.txt','reset_post_history')
    error = Logger('error_log.txt', 'reset_post_history')

    route_history = []
    log.text('Cleared route history.')

    def write_route_history(route_history_list):
        pickle.dump(route_history_list, open("data/post_history.p", "wb+"))
        log.text('Route history saved to disk.')

    try:
        # check for directory and save
        if os.path.isdir('data/'):
            write_route_history(route_history)
        else:
            # create directory
            os.makedirs(os.path.dirname('data/'), exist_ok=True)
            log.text('Data directory not found, creating now.')
            write_route_history(route_history)
    except Exception as ex:
        error.text(f'Failed to save route history: {ex}')

