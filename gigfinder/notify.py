import requests
import os

MG_API_DOMAIN = os.environ['MAILGUN_API_DOMAIN']
NOTIFY_EMAIL = os.environ['NOTIFY_EMAIL_ADDRESS']
MG_API_KEY = os.environ['MAILGUN_API_KEY']


def lambda_handler(event, context):
    for gig in event['Records']:
        if gig['eventName'] == 'INSERT':
            date = list(gig['dynamodb']['NewImage']['date'].values())[0]
            artist = list(gig['dynamodb']['NewImage']['artist'].values())[0]
            venue = list(gig['dynamodb']['NewImage']['venue'].values())[0]
            link = list(gig['dynamodb']['NewImage']['link'].values())[0]
            newline = '\n'
            subject = f'Gig found: {artist}'
            body = f'Date: {date}{newline}Artist: {artist}{newline}Venue: {venue}{newline}Link: {link}{newline}'            
            dispatch_email(subject, body)


def dispatch_email(subject, body):
    notification_email = requests.post(
        "https://api.mailgun.net/v3/" + MG_API_DOMAIN + "/messages",
        auth=("api", MG_API_KEY),
        data={
            "from": "Gig Finder <mailgun@" + MG_API_DOMAIN + ">",
            "to": NOTIFY_EMAIL,
            "subject": subject,
            "text": body,
        },
    )
    print(notification_email)
