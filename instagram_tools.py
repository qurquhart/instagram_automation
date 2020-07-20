import time
import autoit
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def insta_post(ig_username, ig_password, filepath, post_description):
    '''post to instagram using selenium/chrome'''

    def loading_time():
        '''wait for the page to load'''
        time.sleep(2)

    # set chrome settings to emulate mobile device
    mobile_emulation = {
        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D)"\
            " AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(
        'chromedriver.exe', chrome_options=chrome_options)

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

    # submit button
    driver.find_element_by_xpath(
        """//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()
