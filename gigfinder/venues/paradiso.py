import requests
from common import notify_checker


def paradiso(event, context):
    data = collect()
    notify_checker(data)


def date_formatter(raw_date):
    date_data = str(raw_date)
    day = date_data[8:10]
    month = date_data[5:7]
    year = '2020'
    date = f'{day}-{month}-{year}'
    return date


def collect():
    url = "https://api.paradiso.nl/api/events?lang=en&start_time=now&sort=date&order=asc&limit=600&page=1"
    page = requests.get(url)
    gigs = page.json()
    gigs_list = []
    venue = 'paradiso'
    for gig in gigs:
        date = date_formatter(gig['start_date_time'])
        artist = gig['title']
        description = gig['subtitle']
        ticket_url = gig['ticket_url']
        uid = f'{artist}_{date}_{venue}'
        gig = {"id": uid,
               "venue": venue,
               "date": date,
               "artist": artist,
               "link": ticket_url,
               }
        gigs_list.append(new_gig)
    return gigs_list
