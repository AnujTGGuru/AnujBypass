import re
import base64
import requests
from urllib.parse import urlparse, parse_qs
from os import environ

url = open('1.txt', 'r').read()
crypt = environ.get('GDTOT_CRYPT')

print("You have Entered:")
print("URL:")
print(url)
print("Crypt:")
print(crypt)

# ==========================================
print("Bypassing Link...")
def parse_info(res):
    title = re.findall(">(.*?)<\/h5>", res.text)[0]
    info = re.findall('<td\salign="right">(.*?)<\/td>', res.text)
    parsed_info = {
        'error': True,
        'message': 'Link Invalid.',
        'title': title,
        'size': info[0],
        'date': info[1]
    }
    return parsed_info

# ==========================================

def gdtot_dl(url):
    client = requests.Session()
    client.cookies.update({ 'crypt': crypt })
    res = client.get(url)

    info = parse_info(res)
    info['src_url'] = url
    
    res = client.get(f"https://new.gdtot.top/dld?id={url.split('/')[-1]}")

    try:
        url = re.findall('URL=(.*?)"', res.text)[0]
        print(url)
    except:
        info['message'] = 'The requested URL could not be retrieved.',
        return info

    params = parse_qs(urlparse(url).query)
    
    if 'msgx' in params:
        info['message'] = params['msgx'][0]
    
    if 'gd' not in params or not params['gd'] or params['gd'][0] == 'false':
        return info
    
    try:
        decoded_id = base64.b64decode(str(params['gd'][0])).decode('utf-8')
        gdrive_url = f'https://drive.google.com/open?id={decoded_id}'
        info['message'] = 'Success.'
    except:
        info['error'] = True
        return info

    info['gdrive_link'] = gdrive_url
    
    return info['gdrive_link']
    
# ==========================================

info = gdtot_dl(url)

print("❤️✨GOOGLE DRIVE LINK: "+ info + " ❤️✨" ,file=open("2.txt", "w"))
print("Bypassed Successfully!")
