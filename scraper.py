import re
import csv
import sys
import requests
from datetime import datetime,timezone

response = requests.get('https://www.instagram.com/marounbaydoun?hl=en')
html = response.text

follower_matches = re.search('\"edge_followed_by\":\{"count":(\d+)\}', html)
following_matches = re.search('\"edge_follow\":\{"count":(\d+)\}', html)

follower_count = follower_matches.group(1) if follower_matches else None
following_count = following_matches.group(1) if following_matches else None


if follower_count is None or following_count is None:
    sys.exit(0)

now_utc = datetime.now(timezone.utc)
fields=[now_utc.isoformat(), follower_count, following_count]


with open(f'data/{now_utc.month}-{now_utc.year}.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
