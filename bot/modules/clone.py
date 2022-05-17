import random
import string
from threading import Thread
from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup, ParseMode, InlineKeyboardButton
from threading import Thread
from time import sleep

from bot.helper.clone_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.clone_utils.status_utils.clone_status import CloneStatus
from bot import dispatcher, LOGGER, CLONE_LIMIT, STOP_DUPLICATE, download_dict, download_dict_lock, Interval, CLONE_LOGS, BOT_PM, CHANNEL_USERNAME, bot, FSUB_CHANNEL_ID, FSUB, AUTO_DELETE_UPLOAD_MESSAGE_DURATION
from bot.helper.ext_utils.bot_utils import get_readable_file_size, is_gdrive_link, is_gdtot_link, is_appdrive_link, is_driveapp_link, is_gdflix_link, is_drivebit_link, is_drivelinks_link, is_drivesharer_link, is_hubdrive_link, is_katdrive_link, is_kolop_link, is_drivefire_link, new_thread
from bot.helper.clone_utils.download_utils.direct_link_generator import gdtot, appdrive, driveapp, gdflix, drivebit, drivelinks, drivesharer, hubdrive, katdrive, kolop, drivefire
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def new_thread(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper

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

def is_gdrive_link(url: str):
    return "drive.google.com" in url

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

def is_driveliks_link(url: str):
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
    
@new_thread
def cloneNode(update, context, multi=0):
    if AUTO_DELETE_UPLOAD_MESSAGE_DURATION != -1:
        reply_to =update.message.reply_to_message
        if reply_to is not None:
            reply_to.delete()
    if FSUB:
        try:
            uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
            user = bot.get_chat_member(f"{FSUB_CHANNEL_ID}", update.message.from_user.id)
            LOGGER.error(user.status)
            if user.status not in ('member', 'creator', 'administrator'):
                buttons = ButtonMaker()
                buttons.buildbutton("Click Here To Join Updates Channel", f"https://t.me/{CHANNEL_USERNAME}")
                reply_markup = InlineKeyboardMarkup(buttons.build_menu(1))
                message = sendMarkup(str(f"️<b>Dear {uname}, You haven't join our Updates Channel yet.</b>\n\nKindly Join @{CHANNEL_USERNAME} To Use Bots. "), bot, update, reply_markup)
                Thread(target=auto_delete_upload_message, args=(bot, update.message, message)).start()
                return
        except:
            pass
    if BOT_PM:
        try:
            msg1 = f'Added your Requested link to clone\n'
            send = bot.sendMessage(update.message.from_user.id, text=msg1,)
            send.delete()
        except Exception as e:
            LOGGER.warning(e)
            bot_d = bot.get_me()
            b_uname = bot_d.username
            uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
            channel = CHANNEL_USERNAME
            botstart = f"http://t.me/{b_uname}"
            keyboard = [
                [InlineKeyboardButton("Click Here to Start Me", url=f"{botstart}")]]
            message = sendMarkup(
                f"Dear {uname},\n\n<b>I found that you haven't started me in PM (Private Chat) yet.</b>\n\nFrom now on i will give link and leeched files in PM and log channel only.",
                bot, update, reply_markup=InlineKeyboardMarkup(keyboard))
            Thread(target=auto_delete_message, args=(bot, update.message, message)).start()
            return
    args = update.message.text.split(" ", maxsplit=1)
    reply_to = update.message.reply_to_message
    link = ''
    if len(args) > 1:
        link = args[1]
        if link.isdigit():
            multi = int(link)
            link = ''
        elif update.message.from_user.username:
            tag = f"@{update.message.from_user.username}"
        else:
            tag = update.message.from_user.mention_html(update.message.from_user.first_name)
    elif reply_to is not None:
        if len(link) == 0:
            link = reply_to.text
        if reply_to.from_user.username:
            tag = f"@{reply_to.from_user.username}"
        else:
            tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)
    is_gdtot = is_gdtot_link(link)
    is_appdrive = is_appdrive_link(link)
    is_driveapp = is_driveapp_link(link)
    is_gdflix = is_gdflix_link(link)
    is_drivebit = is_drivebit_link(link)
    is_drivelinks = is_drivelinks_link(link)
    is_drivesharer = is_drivesharer_link(link)
    is_hubdrive = is_hubdrive_link(link)
    is_katdrive = is_katdrive_link(link)
    is_kolop = is_kolop_link(link)
    is_drivefire = is_drivefire_link(link)
    if is_gdtot:
        msg = sendMessage(f"✨✨GDTOT Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = gdtot(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)
    elif is_appdrive:
        msg = sendMessage(f"✨✨AppDrive Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = appdrive(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)
    elif is_driveapp:
        msg = sendMessage(f"✨✨DriveApp Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = driveapp(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)     
    elif is_gdflix:
        msg = sendMessage(f"✨✨GDFlix Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = gdflix(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)  
    elif is_drivebit:
        msg = sendMessage(f"✨✨DriveBit Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = drivebit(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)  
    elif is_drivelinks:
        msg = sendMessage(f"✨✨DriveLinks Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = drivelinks(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)  
    elif is_drivesharer:
        msg = sendMessage(f"✨✨DriveSharer Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = drivesharer(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)  
    if is_hubdrive:
        msg = sendMessage(f"✨✨HubDrive Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = hubdrive(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)
    if is_katdrive:
        msg = sendMessage(f"✨✨KatDrive Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = katdrive(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)
    if is_kolop:
        msg = sendMessage(f"✨✨KOLOP Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = kolop(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)
    if is_drivefire:
        msg = sendMessage(f"✨✨DriveFire Link Detected✨✨ !\nBypassing: <code>{link}</code>", context.bot, update)
        try:
            link = drivefire(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)
    if is_gdrive_link(link):
        gd = GoogleDriveHelper()
        res, size, name, files = gd.helper(link)
        if res != "":
            return sendMessage(res, context.bot, update)
        if STOP_DUPLICATE:
            LOGGER.info('Checking File/Folder if already in Drive...')
            smsg, button = gd.drive_list(name, True, True)
            if smsg:
                msg3 = "File/Folder is already available in Drive.\nHere are the search results:"
                return sendMarkup(msg3, context.bot, update, button)
        if CLONE_LIMIT is not None:
            LOGGER.info('Checking File/Folder Size...')
            if size > CLONE_LIMIT * 1024**3:
                msg2 = f'Failed, Clone limit is {CLONE_LIMIT}GB.\nYour File/Folder size is {get_readable_file_size(size)}.'
                return sendMessage(msg2, context.bot, update)
        if multi > 1:
            sleep(1)
            nextmsg = type('nextmsg', (object, ), {'chat_id': message.chat_id, 'message_id': message.reply_to_message.message_id + 1})
            nextmsg = sendMessage(args[0], bot, nextmsg)
            nextmsg.from_user.id = message.from_user.id
            multi -= 1
            sleep(1)
            Thread(target=_clone, args=(nextmsg, bot, multi)).start()
        if files <= 20:
            msg = sendMessage(f"Cloning: <code>{link}</code>", context.bot, update)
            result, button = gd.clone(link)
            deleteMessage(context.bot, msg)
        else:
            drive = GoogleDriveHelper(name)
            gid = ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=12))
            clone_status = CloneStatus(drive, size, update, gid)
            with download_dict_lock:
                download_dict[update.message.message_id] = clone_status
            sendStatusMessage(update, context.bot)
            result, button = drive.clone(link)
            with download_dict_lock:
                del download_dict[update.message.message_id]
                count = len(download_dict)
            try:
                if count == 0:
                    Interval[0].cancel()
                    del Interval[0]
                    delete_all_messages()
                else:
                    update_all_messages()
            except IndexError:
                pass
        cc = f'\n\n<b>#Cloned By: </b>{tag}'
        if button in ["cancelled", ""]:
            sendMessage(f"{tag} {result}", context.bot, update)
        else:
            if AUTO_DELETE_UPLOAD_MESSAGE_DURATION != -1:
                auto_delete_message = int(AUTO_DELETE_UPLOAD_MESSAGE_DURATION / 60)
                if update.message.chat.type == 'private':
                    warnmsg = ''
                else:
                    warnmsg = f'\n<b>This message will be deleted in <i>{auto_delete_message} minutes</i> from this group.</b>\n'
        if BOT_PM and update.message.chat.type != 'private':
            pmwarn = f"\n<b>I have sent links in PM.</b>\n"
        elif update.message.chat.type == 'private':
            pmwarn = ''
        else:
            pmwarn = ''
        uploadmsg = sendMarkup(result + cc + pmwarn + warnmsg, context.bot, update, button)
        Thread(target=auto_delete_upload_message, args=(bot, update.message, uploadmsg)).start()
        if is_gdtot:
            gd.deletefile(link)
        elif is_appdrive:
            gd.deletefile(link)
        elif is_driveapp:
            gd.deletefile(link)
        elif is_gdflix:
            gd.deletefile(link)
        elif is_drivebit:
            gd.deletefile(link)
        elif is_drivelinks:
            gd.deletefile(link)
        elif is_drivesharer:
            gd.deletefile(link)
        elif is_hubdrive:
            gd.deletefile(link)
        elif is_katdrive:
            gd.deletefile(link)
        elif is_kolop:
            gd.deletefile(link)
        elif is_drivefire:
            gd.deletefile(link)
        if MIRROR_LOGS:
            try:
                for i in MIRROR_LOGS:
                    bot.sendMessage(chat_id=i, text=result + cc, reply_markup=button, parse_mode=ParseMode.HTML)
            except Exception as e:
                LOGGER.warning(e)
            if BOT_PM and update.message.chat.type != 'private':
                try:
                    bot.sendMessage(update.message.from_user.id, text=result, reply_markup=button, parse_mode=ParseMode.HTML)
                except Exception as e:
                    LOGGER.warning(e)
                    return
    else:
        message = sendMessage('Send Gdrive or gdtot link along with command or by replying to the link by command',
                              context.bot, update)
        Thread(target=auto_delete_message, args=(bot, update.message, message)).start()

clone_handler = CommandHandler(BotCommands.CloneCommand, cloneNode, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(clone_handler)
