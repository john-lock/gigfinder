import requests
from bs4 import BeautifulSoup


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
    full_date = f'{month}/{raw_day}'
    return full_date


def collect():
    print("collecting Paard gigs")
    url = "https://www.paard.nl/event/?filter1=concert"
    gigs_list = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    gigs = soup.find_all("div", {"class": "event"})
    venue = 'Paard'
    for gig in gigs:
        event_tags = gig['data-filter1']
        if event_tags == 'concert':
            new_gig = {}
            day = gig.parent.parent.div.em.text
            month = gig.parent.parent.div.text[-3:]
            date = date_formatter(day, month)
            artist = gig.a.h2.text
            description = gig.p.get_text()
            url = gig.a['href']
            uid = str(date + artist + venue)

            new_gig = {uid: {"venue": venue,
                             "date": date,
                             "artist": artist,
                             "description": description,
                             "url": url
                             }}
            gigs_list.append(gig)
    print(len(gigs_list), 'gigs found for Paard')
    return gigs_list


if __name__ == '__main__':
    collect()
