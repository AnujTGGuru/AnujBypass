from re import match, findall
from threading import Thread, Event
from time import time
from math import ceil
from html import escape
from psutil import virtual_memory, cpu_percent, disk_usage
from requests import head as rhead
from urllib.request import urlopen
from telegram import InlineKeyboardMarkup

from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import download_dict, download_dict_lock, STATUS_LIMIT, botStartTime, DOWNLOAD_DIR
from bot.helper.telegram_helper.button_build import ButtonMaker

URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"

COUNT = 0
PAGE_NO = 1

class BotStatus:
    STATUS_CLONING = "Cloning...♻️"

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = Event()
        thread = Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time() + self.interval
        while not self.stopEvent.wait(nextTime - time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()

def getAllDownload(req_status: str):
    with download_dict_lock:
        for dl in list(download_dict.values()):
            status = dl.status()
            if req_status == 'clone' and status == BotStatus.STATUS_CLONING:
                  return dl
    return None
  
def get_readable_message():
    with download_dict_lock:
        msg = ""
        if STATUS_LIMIT is not None:
            tasks = len(download_dict)
            global pages
            pages = ceil(tasks/STATUS_LIMIT)
            if PAGE_NO > pages and pages != 0:
                globals()['COUNT'] -= STATUS_LIMIT
                globals()['PAGE_NO'] -= 1
        for index, download in enumerate(list(download_dict.values())[COUNT:], start=1):
            msg += f"<b>Name:</b> <code>{escape(str(download.name()))}</code>"
            msg += f"\n<b>Status:</b> <i>{download.status()}</i>"
            msg += f"\n{get_progress_bar_string(download)} {download.progress()}"
            msg += f"\n<b>Cloned:</b> {get_readable_file_size(download.processed_bytes())}\n<b>Total Size:</b> {download.size()}"
            msg += f"\n<b>👥 User:</b> {download.message.from_user.first_name}(<code>{download.message.from_user.id}</code>)\n<b>⚠️ Warn:</b> <code>/warn {download.message.from_user.id}</code>\n<code>/{BotCommands.CancelClone} {download.gid()}</code>\n___________________________"
            msg += f"\n<b>Size: </b>{download.size()}"
            if STATUS_LIMIT is not None and index == STATUS_LIMIT:
                break
            bmsg = f"<b>CPU:</b> {cpu_percent()}% | <b>FREE:</b> {get_readable_file_size(disk_usage(DOWNLOAD_DIR).free)}"
            bmsg += f"\n<b>RAM:</b> {virtual_memory().percent}% | <b>UPTIME:</b> {get_readable_time(time() - botStartTime)}"
            if STATUS_LIMIT is not None and tasks > STATUS_LIMIT:
              msg += f"<b>Page:</b> {PAGE_NO}/{pages} | <b>Tasks:</b> {tasks}\n"
              buttons = ButtonMaker()
              buttons.sbutton("Previous", "status pre")
              buttons.sbutton("Next", "status nex")
              button = InlineKeyboardMarkup(buttons.build_menu(2))
              return msg + bmsg, button
          return msg + bmsg, ""
        
def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'
    
def get_progress_bar_string(status):
    completed = status.processed_bytes() / 8
    total = status.size_raw() / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 8
    p_str = '■' * cFull
    p_str += '□' * (12 - cFull)
    p_str = f"[{p_str}]"
    return p_str
  
def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result
  
def turn(data):
    try:
        with download_dict_lock:
            global COUNT, PAGE_NO
            if data[1] == "nex":
                if PAGE_NO == pages:
                    COUNT = 0
                    PAGE_NO = 1
                else:
                    COUNT += STATUS_LIMIT
                    PAGE_NO += 1
            elif data[1] == "pre":
                if PAGE_NO == 1:
                    COUNT = STATUS_LIMIT * (pages - 1)
                    PAGE_NO = pages
                else:
                    COUNT -= STATUS_LIMIT
                    PAGE_NO -= 1
        return True
    except:
        return False
      
def is_url(url: str):
    url = findall(URL_REGEX, url)
    return bool(url)  
  
def is_gdtot_link(url: str):
    url = match(r'https?://.+\.gdtot\.\S+', url)
    return bool(url)
  
def is_appdrive_link(url: str):
    url = match(r'https?://(?:\S*\.)?(?:appdrive)\.\S+', url)
    return bool(url)
  
def is_driveapp_link(url: str):
    url = match(r'https?://(?:\S*\.)?(?:driveapp)\.\S+', url)
    return bool(url)
  
def is_gdflix_link(url: str):
    url = match(r'https?://(?:\S*\.)?(?:gdflix)\.\S+', url)
    return bool(url)  
  
def is_drivelinks_link(url: str):
    url = match(r'https?://(?:\S*\.)?(?:drivelinks)\.\S+', url)
    return bool(url)
  
def is_drivebit_link(url: str):
    url = match(r'https?://(?:\S*\.)?(?:drivebit)\.\S+', url)
    return bool(url)
  
def is_drivesharer_link(url: str):
    url = match(r'https?://(?:\S*\.)?(?:drivesharer)\.\S+', url)
    return bool(url)
  
def is_hubdrive_link(url: str):
    url = match(r'https?://(?:\S*\.)?(?:hubdrive)\.\S+', url)
    return bool(url)
  
def is_katdrive_link(url: str):
    url = match(r'https?://(?:\S*\.)?(?:katdrive)\.\S+', url)
    return bool(url)
  
def is_kolop_link(url: str):
    url = match(r'https?://(?:\S*\.)?(?:kolop)\.\S+', url)
    return bool(url)
  
def is_drivefire_link(url: str):
    url = match(r'https?://(?:\S*\.)?(?:drivefire)\.\S+', url)
    return bool(url)
  
def new_thread(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
  
def get_content_type(link: str) -> str:
    try:
        res = rhead(link, allow_redirects=True, timeout=5, headers = {'user-agent': 'Wget/1.12'})
        content_type = res.headers.get('content-type')
    except:
        try:
            res = urlopen(link, timeout=5)
            info = res.info()
            content_type = info.get_content_type()
        except:
            content_type = None
    return content_type
