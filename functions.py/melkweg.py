import datetime
import requests
import json
from bs4 import BeautifulSoup

# import boto3
# dynamo resource
# def lambda_handler(event, context):


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
                date = datetime.fromtimestamp(event['date'])
                artist = event['name']
                # gig['ticket_url']
                uid = str(date + artist + venue)
                gig = {uid: {"venue": venue,
                             "date": date,
                             "artist": artist,
                             }}
                gigs_list.apped(gig)

collect()
