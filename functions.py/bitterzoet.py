import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os


def date_formatter(date, raw_month):
    months = {'JANUARI': '01',
              'FEBRUARI': '02',
              'MAART': '03',
              'APRIL': '04',
              'MEI': '05',
              'JUNI': '06',
              'JULI': '07',
              'AUGUSTUS': '08',
              'SEPTEMBER': '09',
              'OKTOBER': '10',
              'NOVEMBER': '11',
              'DECEMBER': '12'
              }
    if str(raw_month) in months:
        month = months[raw_month]
        full_date = f'{month}/{date}'
        return full_date
    else:
        return 'this week'


def collect():
    print("collecting Bitterzoet gigs")
    url = "https://www.bitterzoet.com/agenda/"
    gigs_list = []
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(3)

    elem = browser.find_element_by_tag_name("body")

    no_of_pagedowns = 20

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)
        no_of_pagedowns -= 1

    posts = browser.find_elements_by_class_name("agenda-page__agenda-item")

    venue = 'Bitterzoet'
    for post in posts:
        gig = {}
        entry_data = post.text
        word_split = entry_data.split()
        date = date_formatter(word_split[1], word_split[2])
        line_split = entry_data.split('\n')
        artist = line_split[1]
        description = line_split[2]
        uid = str(date + artist + venue)

        gig = {uid: {"venue": venue,
                     "date": date,
                     "artist": artist,
                     "description": description,
                     }}
        gigs_list.append(gig)

    browser.quit()
    print(len(gigs_list), 'gigs found at Bitterzoet')
    return gigs_list
