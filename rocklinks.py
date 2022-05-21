import time
import cloudscraper
from bs4 import BeautifulSoup 

url = open('1.txt', 'r').read()
print("You Have Entered:")
print(url)
print("Checking Link!")

# ---------------------------------------------------------------------------------------------------------------------

def rocklinks_bypass(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    
    if 'spidermods.in' in url:
      DOMAIN = "https://links.spidermods.in/"
    elif 'rocklink.in' in url:
      DOMAIN = "https://rocklink.in/"
    elif 'rocklinks.net' in url:
      DOMAIN = "https://links.spidermods.in/"
    else:
      return print("Invalid Link")

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}?quelle="

    resp = client.get(final_url)
    
    soup = BeautifulSoup(resp.content, "html.parser")
    try:
        inputs = soup.find(id="go-link").find_all(name="input")
    except:
        return "Incorrect Link"
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(6)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

# -----------------------------------
inf = rocklinks_bypass(url)
print("❤️✨𝗕𝘆𝗽𝗮𝘀𝘀𝗲𝗱 𝗥𝗼𝗰𝗸𝗹𝗶𝗻𝗸𝘀: "+ inf + " ❤️✨" ,file=open("2.txt", "w"))
