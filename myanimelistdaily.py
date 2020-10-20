import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re


def animeschedule():
    ret=[]
    URL = 'https://myanimelist.net/anime/season/schedule'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(class_='seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-monday clearfix')

    for results in results:
        data=[]
        if isinstance(results,NavigableString):
            continue
        animename=results.find('h2', class_='h2_anime_title')
        synopsis=results.find('div', class_='synopsis js-synopsis')
        images=results.find('img', {'src':re.compile('.jpg')})
        if None in (animename,images,synopsis):
            continue
        data.append(animename.text)
        data.append(images['src'])
        data.append(synopsis.text)
        ret.append(data)
    return ret



