import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
from datetime import date

todays = date.today().weekday()
weekday=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
day=weekday[todays+1]

def animeschedule():
    ret=[]
    URL = 'https://myanimelist.net/anime/season/schedule'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    
    classname='seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-'+day+' clearfix'
    results = soup.find(class_=classname)
    print(day)
    for results in results:
        data=[]
        if isinstance(results,NavigableString):
            continue
        animename=results.find('h2', class_='h2_anime_title')
        classs=results.find('div', class_='image')
        if None in (animename,classs):
            continue
        
        if day=='monday':
            images=classs.find('img', {'src':re.compile('.jpg')})
            print(images['src'])
            data.append(animename.text)
            data.append(images['src'])
        else:
            images=classs.find('img', {'data-src':re.compile('.jpg')})
            print(images['data-src'])
            data.append(animename.text)
            data.append(images['data-src'])
        ret.append(data)
    return ret




