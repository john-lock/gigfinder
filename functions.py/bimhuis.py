import requests
from bs4 import BeautifulSoup


def date_formatter(raw_date):
    date_data = raw_date.split()
    date = date_data[1]
    months = {'January': '01',
              'February': '02',
              'March': '03',
              'April': '04',
              'May': '05',
              'June': '06',
              'July': '07',
              'August': '08',
              'September': '09',
              'October': '10',
              'November': '11',
              'December': '12'
              }
    month = months[date_data[2]]
    full_date = f'{month}/{date}'
    return full_date


def date_formatter_backup_bimhuis(raw_date):
    date_data = raw_date.split()
    date = date_data[1]
    months = {'JANUARI': '01',
              'FEBRUARI': '02',
              'MAART': '03',
              'APRIL': '04',
              'MEI': '05',
              'JUNI': '06',
              'JULI': '07',
              'AUGUSTUS': '08',
              'SEPTEMBER': '09',
              'OKTOBER': '10',
              'NOVEMBER': '11',
              'DECEMBER': '12'
              }
    month = months[str(date_data[2]).upper()]
    year = date_data[3]
    full_date = f'{month}/{date}/{year}'
    return full_date


def collect():
    print("Collecting Bimhuis gigs")
    try:
        url = "https://www.bimhuis.nl/agenda/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        gigs = soup.find_all("div", {"class": "content"})
        formatted_gigs = formatter('Bimhuis', gigs)

    except IOError:
        print('Trying backup URL for Bimhuis')
        url = 'https://muziekladder.nl/nl/locaties/bimhuis-Amsterdam'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        gigs = soup.find_all('div', {'class': 'event clearfix'})
        formatted_gigs = formatter('muziekladder', gigs)

    finally:
        print(len(formatted_gigs), 'gigs found for Bimhuis')
        return formatted_gigs


def formatter(site, gigs):
    venue = 'Bimhuis'
    gigs_list = []
    if site == 'bimhuis':
        for i in range(len(gigs)):
            gig = {}
            date = date_formatter(gigs[i].div.get_text())
            artist = str(gigs[i].h3)[4:-5]
            description = str(gigs[i].p.get_text())
            uid = str(date + artist + venue)

            gig = {uid: {"venue": venue,
                         "date": date,
                         "artist": artist,
                         "description": description,
                         }}
            gigs_list.append(gig)
        return gigs_list
    else:
        for i in range(len(gigs)):
            gig = {}
            date = date_formatter_backup_bimhuis(gigs[i].a.get_text())
            artist = gigs[i].span.get_text()
            uid = str(date + artist + venue)

            gig = {uid: {"venue": venue,
                         "date": date,
                         "artist": artist,
                         }}
            gigs_list.append(gig)
    return gigs_list
