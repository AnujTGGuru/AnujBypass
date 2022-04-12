import time
import requests
from bs4 import BeautifulSoup 

url = open('1.txt', 'r').read()

# -----------------------------------

def rocklinks_bypass(url):
    client = requests.Session()
    DOMAIN = "https://link.techyone.co"
    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}?quelle="

    resp = client.get(final_url)
    
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find(id="go-link").find_all(name="input")
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(6)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

# -----------------------------------

print(rocklinks_bypass(url) ,file=open("2.txt", "w"))
print("Confirming Link...")
print("Successfully Bypassed!")
