print("Setting Up!")
print("Performing Check...")
import time
import requests
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse
print("Everything Looks Good! Lets Continue.")


url = open('1.txt', 'r').read()
print("Entered Link:")
print(url)
print("Checking Link...")
print("Checking Done!")
# ==============================================
print("Bypassing the Link...")
def gplinks_bypass(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    res = client.head(url)
    header_loc = res.headers['location']
    param = header_loc.split('postid=')[-1]
    req_url = f'{p.scheme}://{p.netloc}/{param}'

    p = urlparse(header_loc)
    ref_url = f'{p.scheme}://{p.netloc}/'

    h = { 'referer': ref_url }
    res = client.get(req_url, headers=h, allow_redirects=False)

    bs4 = BeautifulSoup(res.content, 'html.parser')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'referer': ref_url,
        'x-requested-with': 'XMLHttpRequest',
    }
    time.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    return res.json()['url'].replace('\/','/')
# ==============================================

inf = gplinks_bypass(url)
print("❤️✨BYPASSED GPLINKS LINK: "+ inf + " ❤️✨" ,file=open("2.txt", "w"))
print("Confirming Link...")
print("Successfully Bypassed!")
