import boto3
from botocore.exceptions import ClientError
import datetime
import requests
from data import tracked_artists

dynamodb = boto3.resource('dynamodb')


def melkweg(event, context):
    table = dynamodb.Table("gf_db")
    data = collect()
    for gig in data:
        if gig['artist'].lower() in tracked_artists:
            try:
                table.put_item(
                    Item={'id': gig['id'],
                          'artist': gig['artist'],
                          'venue': gig['venue'],
                          'date': gig['date'],
                          'ticket_url': gig['ticket_url'],
                          },
                    ConditionExpression='attribute_not_exists(id)'
                )
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
                ticket_url = event.get('ticket_url')
                date = str(datetime.datetime.fromtimestamp(int(event['date'])))
                artist = str(event['name'])
                uid = str(artist + '_' + date[:10] + '_' + venue)
                gig = {"id": uid,
                       "venue": venue,
                       "date": date[:10],
                       "artist": artist,
                       "ticket_url": ticket_url,
                       }
                gigs_list.append(gig)
    return gigs_list
