import boto3
import json
import requests
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup
from data import tracked_artists


def paard(event, context):
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
                          'link': gig['link']
                          },
                    ConditionExpression='attribute_not_exists(id)'
                )
            except ClientError as e:
                if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                    raise


def date_formatter(raw_day, raw_month):
    months = {'jan': '01',
              'feb': '02',
              'mrt': '03',
              'apr': '04',
              'mei': '05',
              'jun': '06',
              'jul': '07',
              'aug': '08',
              'sep': '09',
              'okt': '10',
              'nov': '11',
              'dec': '12'
              }
    month = months[raw_month]
    year = '2020'
    full_date = f'{raw_day}-{month}-{year}'
    return full_date


def collect():
    url = "https://www.paard.nl/event/?filter1=concert"
    gigs_list = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    gigs = soup.find_all("div", {"class": "event"})
    venue = 'paard'
    for gig in gigs:
        event_tags = gig['data-filter1']
        if event_tags == 'concert':
            day = gig.parent.parent.div.em.text
            month = gig.parent.parent.div.text[-3:]
            date = date_formatter(day, month)
            artist = gig.a.h2.text
            link = gig.a['href']
            uid = f'{artist}_{date}_{venue}'

            new_gig = {"id": uid,
                       "venue": venue,
                       "date": date,
                       "artist": artist,
                       "link": link,
                       }
            gigs_list.append(new_gig)
    return gigs_list
