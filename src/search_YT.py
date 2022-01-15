import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import json
import mysql.connector
import undetected_chromedriver.v2 as uc
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import kkbox
GMAIL = 'YOUR GMAIL'
PASSWORD = 'YOUR PASSWORD'
conn = mysql.connector.connect(host='127.0.0.1', port='3306', user='root',
                               password='Qrs133666!', database='rank_list', charset='utf8')
cur = conn.cursor()

if __name__ == '__main__':
    url, song_type = kkbox.GUI()
    table_name = input("Please select or create a table name :")
    kkbox.get_song(url, song_type, table_name)

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("user_agent=DN")
    driver = uc.Chrome(options=chrome_options)
    driver.delete_all_cookies()
    # declare for wait
    wait = WebDriverWait(driver, 3)
    presence = EC.presence_of_element_located
    visible = EC.visibility_of_element_located
    # login with oauthplayground
    # because of the hardness of login google derectly
    driver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
    # account
    driver.find_element(By.XPATH,
                        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(GMAIL)
    driver.find_element(By.XPATH,
                        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(Keys.RETURN)
    time.sleep(5)
    # password
    driver.find_element(By.XPATH,
                        '//html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(PASSWORD)
    driver.find_element(By.XPATH,
                        '//html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(Keys.RETURN)
    time.sleep(10)

    # get data from table
    get_name = "SELECT song_name FROM {} ORDER BY song_rank"
    cur.execute(get_name.format(table_name))
    songs = cur.fetchall()

    for song in songs:
        song_name = song[0]
        driver.get(
            'https://www.youtube.com/results?search_query={}'.format(song_name))
        wait.until(visible((By.ID, "video-title")))
        driver.find_element(By.ID, "video-title").click()
        time.sleep(3)
        driver.find_element(By.LINK_TEXT, '儲存').click()
        time.sleep(3)

        # if driver.find_element(By.XPATH, "/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-add-to-playlist-renderer/div[2]/ytd-playlist-add-to-option-renderer[2]/tp-yt-paper-checkbox").aria-checked == True:
        #     continue
        # else:
        driver.find_elements(By.ID, "checkboxContainer")[1].click()

        time.sleep(3)
    driver.quit()

# driver.find_element(By.ID, "playlists").find_elements(By.TAG_NAME, "ytd-playlist-add-to-option-renderer")[2].find_element(By.ID, "ink")
