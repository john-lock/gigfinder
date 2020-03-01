import requests
from bs4 import BeautifulSoup
from common import notify_checker


def bird(event, context):
    data = collect()
    notify_checker(data)


def date_formatter(raw_date):
    try:
        date_data = raw_date.split()
        day = date_data[1]
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
        formatted_date = f'{day}-{month}-{year}'
    except IndexError:
        formatted_date = '-'
    finally:
        return formatted_date


def collect():
    venue = 'bird'
    url = 'https://bird-rotterdam.nl/en/agenda/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    venue_data = soup.find_all("div", {"class": "isotope"})
    gigs_list = []
    for gigs in venue_data:
        for gig in gigs:
            try:
                artist = gig.h1.text
                raw_date = gig.h2.text
                date = date_formatter(raw_date)
                link = gig.a['href']
                uid = f'{artist}_{date}_{venue}'
                new_gig = {"id": uid,
                           "venue": venue,
                           "date": date,
                           "artist": artist,
                           }
                gigs_list.append(new_gig)
            except AttributeError:
                pass
    return gigs_list
