import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import json
import mysql.connector
import table


conn = mysql.connector.connect(host='127.0.0.1', port='3306', user='root',
                               password='MYSQLPASSWORD', database='rank_list', charset='utf8')
cur = conn.cursor()
# 390 English
# 297 華語
# type = song || newrelease


def get_song(url, song_type, table_name):

    response = requests.get(url)
    data = json.loads(response.text)
    song_list = data["data"]["charts"][song_type]  # [newrelease]
    song_name_list = []
    for song in song_list:
        song_rank = song["rankings"]["this_period"]
        song_name = song["song_name"]
        song_name_list.append(song_name)
        song_url = song["song_url"]
        song_artist = song["artist_name"]
        # 用time.strftime()函數從timestamp轉為人類習慣的日期格式(年-月-日)。
        song_date = time.strftime(
            "%Y-%m-%d", time.localtime(song["release_date"]))
        table.create_table(table_name)
        insert = "INSERT INTO {}(song_rank,song_name,song_artist,song_url,song_date) values('%s', '%s', '%s', '%s', '%s' )" \
            % (song_rank, song_name, song_artist, song_url, song_date)
        try:
            # Execute the SQL command
            cur.execute(insert.format(table_name))
            # Commit your changes in the database
            conn.commit()
        except:
            # Rollback in case there is any error
            conn.rollback()

        # print("排名:", song_rank)
        # print("歌名:", song_name)
        # print("連結:", song_url)
        # print("作者:", song_artist)
        # print("發行日期:", song_date)
        # print("-------------------------")


def GUI():
    url = ""
    print("Please input a date:")
    song_date = input("ex : 2020-12-10\n")
    print("Choose a language of song rank:")
    print("1) Chinese")
    print("2) English")
    print("3) Japanese")
    song_language = input()
    print("Choose a type of song rank:")
    print("1) New release")
    print("2) Single")
    song_type = input()

    if song_language == "1":
        song_language = "297"
    elif song_language == "2":
        song_language = "390"
    elif song_language == "3":
        song_language = "308"
    else:
        print("error input")
        exit()

    if song_type == "1":
        song_type = "newrelease"
    elif song_type == "2":
        song_type = "song"
    else:
        print("error input")
        exit()
    url = "https://kma.kkbox.com/charts/api/v1/daily?category="+song_language + \
        "&date="+song_date+"&lang=tc&limit=50&terr=tw&type="+song_type

    return url, song_type
