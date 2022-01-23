import json
from datetime import datetime

import numpy
import requests


def call():
    url = 'https://api.github.com/users/anthony-chukwuemeka-nwachukwu/repos?sort=created&direction=desc'

    repos = json.loads( requests.get(url).text )

    title, link, desc, date = [], [], [], []

    date_object = lambda x: datetime.strftime(datetime.fromisoformat(x), '%b %d %Y')

    for r in repos:
        title.append(str(r['name']).capitalize())
        link.append(r['svn_url'])
        desc.append(r['description'] if r['description'] is not None else 'Description Not Available')
        date.append(date_object(r['created_at'][:10]))
    img = ["/static/img/platforms/github.jpg" for i in title]
    author = ["Nwachukwu Anthony" for i in title]
    return title, link, desc, author, date, img



