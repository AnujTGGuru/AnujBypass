import re
import requests
from urllib.parse import urlparse
from os import environ

url = open('1.txt', 'r').read()
crypt = environ.get('DRIVEFIRE_CRYPT')

print("You have Entered:")
print("URL:")
print(url)
print("crypt:")
print(crypt)

# ==========================================
print("Bypassing Link...")

def parse_info(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def drivefire_dl(url: str):
    client = requests.Session()
    client.cookies.update({'crypt': crypt})
    
    res = client.get(url)
    info_parsed = parse_info(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    
    data = { 'id': file_id }
    
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    
    decoded_id = res.rsplit('/', 1)[-1]
    info_parsed = f"https://drive.google.com/file/d/{decoded_id}"
    return info_parsed
    
# ==========================================

info = drivefire_dl(url)

print("❤️✨GOOGLE DRIVE LINK: "+ info + " ❤️✨" ,file=open("2.txt", "w"))
print("Bypassed Successfully!")
