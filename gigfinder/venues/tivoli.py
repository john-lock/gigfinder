import requests
from common import notify_checker


def tivoli(event, context):
    data = collect()
    notify_checker(data)


def collect():
    venue = 'tivoli'
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
                link = gig.get('link')
                day = str(gig['day']).split()[1]
                month = str(gig['yearMonth'][-2:])
                year = str(gig['year'])
                date = f'{day}-{month}-{year}'
                artist = str(gig['title'])
                uid = f'{artist}_{date}_{venue}'

                new_gig = {"id": uid,
                           "venue": venue,
                           "date": date,
                           "artist": artist,
                           "link": link,
                           }
                gigs_list.append(new_gig)
    return gigs_list
