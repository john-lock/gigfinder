import boto3
import os
import json
import requests
from bs4 import BeautifulSoup


dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    table = dynamodb.Table("gigs")
    data = collect()
    for gig in data:
        check = table.get_item(Key={'id': gig['id']})
        if check:
            print("check true")
        else:
            print('item not seen before')
            table.put_item(Item={'id': gig['id'], 'artist': gig['artist'], 'venue': gig['venue'], 'date': ['date']})



def date_formatter(raw_date):
    date_data = str(raw_date)
    date = date_data[8:10]
    month = date_data[5:7]
    full_date = f'{month}/{date}'
    return full_date


def collect():
    print("collecting Paradiso gigs")
    url = "https://api.paradiso.nl/api/events?lang=en&start_time=now&sort=date&order=asc&limit=600&page=1"
    page = requests.get(url)
    gigs = page.json()
    gigs_list = []

    venue = 'Paradiso'
    for gig in gigs:
        new_gig = {}
        date = date_formatter(gig['start_date_time'])
        artist = gig['title']
        description = gig['subtitle']
        ticket_url = gig['ticket_url']
        ticket_price = gig['ticket_price']
        uid = str(date + artist + venue)

        new_gig = {uid: {"venue": venue,
                         "date": date,
                         "artist": artist,
                         "description": description,
                         "ticket_url": ticket_url,
                         "ticket_price": ticket_price,
                         }}
        gigs_list.append(new_gig)
    return gigs_list
