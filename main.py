import telegram.ext
import os
from os import environ
import re
import base64
import requests
from urllib.parse import urlparse, parse_qs

TOKEN = environ.get('BOT_TOKEN')

def start(update, context):
    update.message.reply_text("Hello folks! I will bypass the shortlinks and Generate Direct GDrive Link")
    
def help(update, context):
   update.message.reply_text("""
   the following commands are available
/start -> Welcome Message

/help -> all helpful command list

/adf -> bypass adf.ly link

/droplink -> bypass droplink.co link

/gp -> bypass gplink stinky url

/rlb -> bypass rocklinks url

/lv -> linkvertise link bypass

/gdtot -> GDTOT links (GDTOT CRYPT REQUIRED)

/sd -> AppDrive or DriveApp links (login required wont work for now)

/ex -> use this command for these services
linkvertise.com
exe.io/exey.io
sub2unlock.net/sub2unlock.com
rekonise.com
letsboost.net
ph.apps2app.com
mboost.me
shortconnect.com
sub4unlock.com
ytsubme.com
bit.ly
social-unlock.com
boost.ink
goo.gl
shrto.ml
t.co
tinyurl.com

usage - commands{} link{https://...} (example -->/adf https://adf.ly/xyz)
   """)

def adf(update, context):
        zipk = context.args[0]
        open('1.txt','w').write(zipk)
        update.message.reply_text(f"processing")
        os.system('python bypas.py')
        zkm = open('2.txt', 'r').read()
        update.message.reply_text(f"Done")
        update.message.reply_text(f"{zkm}")
def ex(update, context):
        zipk = context.args[0]
        open('1.txt','w').write(zipk)
        update.message.reply_text(f"processing")
        os.system('python ex.py')
        zkm = open('2.txt', 'r').read()
        update.message.reply_text(f"{zkm}")

def gp(update, context):
        zipk = context.args[0]
        open('1.txt','w').write(zipk)
        update.message.reply_text(f"processing")
        os.system('python gp.py')
        update.message.reply_text(f"Done")
        zkm = open('2.txt', 'r').read()
        update.message.reply_text(f"{zkm}")

def droplink(update, context):
        zipk = context.args[0]
        open('1.txt','w').write(zipk)
        update.message.reply_text(f"processing")
        os.system('python droplink.py')
        zkm = open('2.txt', 'r').read()
        update.message.reply_text(f"{zkm}")

def gdtot(update, context):
        zipk = context.args[0]
        open('1.txt','w').write(zipk)
        update.message.reply_text(f"processing")
        os.system('python gdtot.py')
        zkm = open('2.txt', 'r').read()
        update.message.reply_text(f"{zkm}")
        
def sd(update, context):
        zipk = context.args[0]
        open('1.txt','w').write(zipk)
        update.message.reply_text(f"processing")
        os.system('python sd.py')
        zkm = open('2.txt', 'r').read()
        update.message.reply_text(f"{zkm}")

def lv(update, context):
        zipk = context.args[0]
        open('1.txt','w').write(zipk)
        update.message.reply_text(f"processing")
        os.system('python ex.py')
        zkm = open('2.txt', 'r').read()
        update.message.reply_text(f"{zkm}")
        
def rlb(update, context):
        zipk = context.args[0]
        open('1.txt','w').write(zipk)
        update.message.reply_text(f"processing")
        os.system('python rlb.py')
        update.message.reply_text(f"Done")
        zkm = open('2.txt', 'r').read()
        update.message.reply_text(f"{zkm}")

updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher
disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("help", help))
disp.add_handler(telegram.ext.CommandHandler("adf", adf))
disp.add_handler(telegram.ext.CommandHandler("droplink", droplink))
disp.add_handler(telegram.ext.CommandHandler("gdtot", gdtot))
disp.add_handler(telegram.ext.CommandHandler("sd", sd))
disp.add_handler(telegram.ext.CommandHandler("lv", lv))
disp.add_handler(telegram.ext.CommandHandler("gp", gp))
disp.add_handler(telegram.ext.CommandHandler("ex", ex))
disp.add_handler(telegram.ext.CommandHandler("rlb", rlb))
updater.start_polling()
updater.idle()
