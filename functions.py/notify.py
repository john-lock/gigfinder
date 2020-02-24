import boto3
import os
import json
import requests
from bs4 import BeautifulSoup





# dynamodb = boto3.resource('dynamodb')


# def lambda_handler(event, context):
#     table = dynamodb.Table("gigs")
#     data = collect()
#     for gig in data:
#         check = table.get_item(Key={'id': gig['id']})
#         if check:
#             print("check true")
#         else:
#             print('item not seen before')
#             table.put_item(Item={'id': gig['id'], 'artist': gig['artist'], 'venue': gig['venue'], 'date': ['date']})



# import requests
# import json
# from data.artists import artists_lower
# from config import MG_API_DOMAIN, NOTIFY_EMAIL, MG_API_KEY


# MAILGUN_API_DOMAIN = MG_API_DOMAIN
# NOTIFY_EMAIL_ADDRESS = NOTIFY_EMAIL
# MAILGUN_API_KEY = MG_API_KEY


# def Notify(gig):
#     with open("data/notified.json") as notifyFile:
#         try:
#             data = json.load(notifyFile)
#         except json.decoder.JSONDecodeError:
#             data = {}
#         data.update(gig)

#     email_subject = "Gig found: " + list(gig.values())[0]['artist']
#     email_body = []
#     gig_data = list(gig.values())[0]
#     for i in gig_data.items():
#         email_body.append(i[0] + ': ' + i[1])
#     email_dispatch(email_subject, str(email_body))

#     with open("data/notified.json", "w") as f:
#         json.dump(data, f)


# def notify_checker():
#     print("Checking for new gigs to notify")
#     with open("data/gigs.json") as datafile:
#         all_gigs = json.load(datafile)
#         with open("data/notified.json") as notifiedFile:
#             # To guard against when the notified.json is empty
#             try:
#                 notified_gigs = json.load(notifiedFile)
#             except json.decoder.JSONDecodeError:
#                 notified_gigs = {}

#             for gig in all_gigs:
#                 for gig_id in gig:
#                     if gig[gig_id]["artist"].lower() in artists_lower:
#                         if gig_id not in notified_gigs:
#                             Notify(gig)


# def email_dispatch(subject, body):
#     return requests.post(
#         "https://api.mailgun.net/v3/" + MAILGUN_API_DOMAIN + "/messages",
#         auth=("api", MAILGUN_API_KEY),
#         data={
#             "from": "Gig Finder <mailgun@" + MAILGUN_API_DOMAIN + ">",
#             "to": NOTIFY_EMAIL_ADDRESS,
#             "subject": subject,
#             "text": body,
#         },
#     )
