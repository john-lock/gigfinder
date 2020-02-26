import boto3
from botocore.exceptions import ClientError
import datetime
import requests
import json
from bs4 import BeautifulSoup

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    table = dynamodb.Table("gigs")
    data = collect()
    for gig in data:
        try:
            table.put_item(
                           Item={'id': gig['id'],
                                 'artist': gig['artist'],
                                 'venue': gig['venue'],
                                 'date': gig['date'],
                           },
                           ConditionExpression='attribute_not_exists(id)')
        except ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise


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
                date = str(datetime.datetime.fromtimestamp(int(event['date'])))
                artist = str(event['name'])
                       uid = str(artist + '_' + date[:10] + '_' + venue)
                gig = {"id": uid,
                       "venue": venue,
                       "date": date[:10],
                       "artist": artist,
                       }
                gigs_list.append(gig)
    return gigs_list
