import datetime
import requests
from common import notify_checker


def melkweg(event, context):
    data = collect()
    notify_checker(data)


def collect():
    url = "https://www.melkweg.nl/nl/agenda/as_json/1/grouped/0/page_size/-1?cb=2637334"
    gigs_list = []
    venue = 'melkweg'
    pages = requests.get(url)
    data = pages.json()
    for days in data:
        for event in days['events']:
            event_type = event.get('discipline_name')
            if event_type == 'Concert':
                ticket_url = event.get('ticket_url')
                date = str(datetime.datetime.fromtimestamp(int(event['date'])))
                artist = str(event['name'])
                uid = f'{artist}_{date[:10]}_{venue}'
                gig = {"id": uid,
                       "venue": venue,
                       "date": date[:10],
                       "artist": artist,
                       "link": ticket_url,
                       }
                gigs_list.append(gig)
    return gigs_list
