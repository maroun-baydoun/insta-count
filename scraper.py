import re
import csv
import sys
import requests
import random
from datetime import datetime,timezone


user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Encoding": "gzip, deflate", 
    "Accept-Language": "en-US;q=0.9,en;q=0.8", 
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": random.choice(user_agents)
  }

response = requests.get('https://www.instagram.com/marounbaydoun?hl=en', headers=headers)
html = response.text

print('Fetched HTML')
print(html)

follower_matches = re.search('\"edge_followed_by\":\{"count":(\d+)\}', html)
following_matches = re.search('\"edge_follow\":\{"count":(\d+)\}', html)

follower_count = follower_matches.group(1) if follower_matches else None
following_count = following_matches.group(1) if following_matches else None


if follower_count is None or following_count is None:
    sys.exit(0)

now_utc = datetime.now(timezone.utc)
fields=[now_utc.isoformat(), follower_count, following_count]

print('Will store the following data:', fields)

with open(f'data/{now_utc.month}-{now_utc.year}.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
