import requests
from bs4 import BeautifulSoup
import urllib
import random


def dajare_search(query):
    q_quote = urllib.parse.quote(query)
    r = requests.get(f'https://dajare.jp/keyword/{q_quote}/')
    bs = BeautifulSoup(r.text, features="html.parser")
    dajare = []
    for x in bs.find_all('tr'):
        da = x.find("td", class_='ListWorkBody')
        if not da:
            continue
        score = x.find("td", class_="ListWorkScore")
        dajare.append(
            {'text': da.text, 'score': float(score.text.split(' (')[0])})
    dajare_text = []
    for x in sorted(dajare, key=lambda x: x['score'], reverse=True):
        dajare_text.append(x['text'])
    #result = '\n'.join(dajare_text)
    result = random.choice(dajare_text)
    return result
