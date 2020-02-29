import requests
from bs4 import BeautifulSoup
from common import notify_checker


def bimhuis(event, context):
    data = collect()
    notify_checker(data)


def collect():
    """
    Scrapping the official site even infrequently can lead
    to a fast 24h IP blacklisting so a backup source is sometimes needed.
    """
    try:
        url = "https://www.bimhuis.nl/agenda/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        gigs = soup.find_all("div", {"class": "content"})
        formatted_gigs = bimhuis_formatter(gigs)

    except IOError:
        url = 'https://muziekladder.nl/nl/locaties/bimhuis-Amsterdam'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        gigs = soup.find_all('div', {'class': 'event clearfix'})
        formatted_gigs = muziekladder_formatter(gigs)

    finally:
        return formatted_gigs


def date_formatter(raw_date):
    date_data = raw_date.split()
    date = date_data[1]
    months = {'January': '01',
              'February': '02',
              'March': '03',
              'April': '04',
              'May': '05',
              'June': '06',
              'July': '07',
              'August': '08',
              'September': '09',
              'October': '10',
              'November': '11',
              'December': '12'
              }
    month = months[date_data[2]]
    year = '2020'
    full_date = f'{date}-{month}-{year}'
    return full_date


def date_formatter_backup_bimhuis(raw_date):
    date_data = raw_date.split()
    date = date_data[1]
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
    month = months[str(date_data[2]).upper()]
    year = date_data[3]
    full_date = f'{date}-{month}-{year}'
    return full_date


def bimhuis_formatter(gigs):
    venue = 'bimhuis'
    gigs_list = []
    for i in range(len(gigs)):
        date = date_formatter(gigs[i].div.get_text())
        artist = str(gigs[i].h3)[4:-5]
        uid = f'{artist}_{date}_{venue}'
        gig = {"id": uid,
               "venue": venue,
               "date": date,
               "artist": artist,
               }
        gigs_list.append(gig)
    return gigs_list


def muziekladder_formatter(gigs):
    venue = 'bimhuis'
    gigs_list = []
    for i in range(len(gigs)):
        base_link = "https://muziekladder.nl/nl/gig/?id=4a8362fe6e1353bfbf199f239f20373fe17b3187cf31813ff72d0308_bimhuis&datestring=2020-02-27&g=https%3A%2F%2Fwww.bimhuis.nl%2Fagenda%2Foum-4"
        gig_link = gigs[i].a['href']
        link = f'{base_link}{gig_link}'
        date = date_formatter_backup_bimhuis(gigs[i].a.get_text())
        artist = gigs[i].span.get_text()
        uid = f'{artist}_{date}_{venue}'
        gig = {"id": uid,
               "venue": venue,
               "date": date,
               "artist": artist,
               "link": link,
               }
        gigs_list.append(gig)
    return gigs_list
