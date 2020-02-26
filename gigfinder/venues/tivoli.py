import boto3
import os
import json
import requests
from bs4 import BeautifulSoup
from utils import email_dispatch


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


def collect():
    print("Collecting Tivoli data")
    base_url = "https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&categorie=&maand=&page="
    gigs_list = []
    for i in range(50):
        url = base_url + str(i)
        page = requests.get(url)
        if page.text == 'false':
            break
        else:
            gigs = page.json()
            for gig in gigs:
                day = str(gig['day']).split()[1]
                month = str(gig['yearMonth'][-2:])
                year = str(gig['year'])
                date = f'{day}/{month}/{year}'
                artist = str(gig['title']).replace(" ", "")
                uid = str(f'{artist}_tivoli')

                new_gig = {'id': uid,
                           "venue": 'Tivoli',
                           "date": date,
                           "artist": artist,
                           }
                gigs_list.append(new_gig)
    return gigs_list
