# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import os
import time
import sys
import asyncio
from re import compile
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from telethon.network import ConnectionTcpAbridged
from distutils.util import strtobool as sb
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from dotenv import load_dotenv
from requests import get
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, InviteToChannelRequest
from telethon.sync import TelegramClient, custom
from telethon.tl.functions.users import GetFullUserRequest
from telethon.sessions import StringSession
from telethon.events import callbackquery, InlineQuery, NewMessage
from math import ceil
from datetime import datetime
from telethon.tl.functions.contacts import UnblockRequest

load_dotenv("config.env")

StartTime = time.time()

CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

ASYNC_POOL = []

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - @TheCyberUserBot - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - @TheCyberUserBot - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.info("Ən az Python 3.6 versiyasına sahib olmanız lazımdır."
              "Birdən çox özəllik buna bağlıdır. Bot bağlanır.")
    sys.exit(1)


CONFIG_CHECK = os.environ.get(
    "___________XAIS_______BU_____SETIRI_____SILIN__________", None)

if CONFIG_CHECK:
    LOGS.info(
        "Xahiş edirik ilk hashtag'de qeyd edilən sətiri config.env faylından silin"
    )
    sys.exit(1)

# Bot'un dili
LANGUAGE = os.environ.get("LANGUAGE", "DEFAULT").upper()

if LANGUAGE not in ["EN", "TR", "AZ", "UZ", "DEFAULT", "IN"]:
    LOGS.info("Bilinməyən bir dil yazdınız. Buna görə DEFAULT istifadə edilir.")
    LANGUAGE = "DEFAULT"
    
# CYBER VERSION
CYBER_VERSION = "v4.5"

# SUDO VERSION
SUDO_VERSION = "v1.1"

# Asistan özəlliyi
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
CYBER_BOT = os.environ.get("CYBER_BOT", None)

# API KEY və API HASH
API_KEY = os.environ.get("API_KEY", None)
API_HASH = os.environ.get("API_HASH", None)

try:
    SUDO_ID = {int(x) for x in os.environ.get("SUDO_ID", "").split()}
except ValueError:
    raise Exception("SUDO_ID qeyd etməmisiniz!")
    
SILINEN_PLUGIN = {}

# StringSession
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# Kanal / Grup ID günlüyə qeyd etmə
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", None))

# JARVIS
AUTO_UPDATE =  sb(os.environ.get("AUTO_UPDATE", "True"))

# UserBot log özəlliyi
BOTLOG = sb(os.environ.get("BOTLOG", "False"))
BOTLOG_TAGGER = os.environ.get("BOTLOG_TAGGER", "DEAKTIV")
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "True"))

# Hey! Bu botdur. qorxma ;)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call

# .cyber əmri üçün
CYBER_EMOJI = os.environ.get(
    "CYBER_EMOJI") or "✦ "

# for .salive command
ALIVE_TEXT = os.environ.get(
    "ALIVE_TEXT") or "✦ C Y B Ξ R USERBOT ✦ "

# Zip modulu üçün
ZIP_DOWNLOAD_DIRECTORY = os.environ.get("ZIP_DOWNLOAD_DIRECTORY") or "./zips"

# Güncəlləmə üçün
HEROKU_MEMEZ = sb(os.environ.get("HEROKU_MEMEZ", "False"))
HEROKU_APPNAME = os.environ.get("HEROKU_APPNAME", None)
HEROKU_APIKEY = os.environ.get("HEROKU_APIKEY", None)

# ChatBot
RANDOM_STUFF_API_KEY = os.environ.get("RANDOM_STUFF_API_KEY", None)

# cr: https://github.com/robotlog/SiriUserBot/blob/1c58cb4f61ddc9b9a8f15476d7b1639d9ab3de7d/userbot/__init__.py#L123
STABILITY = sb(os.environ.get("STABILITY", "True"))

# Guncelleme ucun
UPSTREAM_REPO_URL = "https://github.com/CyberUserBot/CyberUserBot.git" if not STABILITY else "https://github.com/FaridDadashzade/CyberUserBot.git"
UPSTREAM_BRANCH = os.environ.get(
    "UPSTREAM_BRANCH") or "master"

# CONSOLE LOGGER VERBOSE
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

# SQL
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///cyber.db")

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", "04889b8e1488957")

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", "HR3T1wqKfoG2QHGhFA9b9nEN")

# AUTO PP
AUTO_PP = os.environ.get("AUTO_PP", None)

# Warn modulu
WARN_LIMIT = int(os.environ.get("WARN_LIMIT", 3))
WARN_MODE = os.environ.get("WARN_MODE", "gmute")

if WARN_MODE not in ["gmute", "gban"]:
    WARN_MODE = "gmute"

# Qalareya
GALERI_SURE = int(os.environ.get("GALERI_SURE", 60))

# Chrome
CHROME_DRIVER = os.environ.get("CHROME_DRIVER", None)
GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)

PLUGINID = os.environ.get("PLUGIN_CHANNEL_ID", None)
# Plugin üçün
if not PLUGINID:
    PLUGIN_CHANNEL_ID = "me"
else:
    PLUGIN_CHANNEL_ID = int(PLUGINID)

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", "d1f00b521eb58c2a2721dfefacc66c3a")
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)

# Anti Spambot
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# SECURITY
DANGERCONFIGS = get('https://raw.githubusercontent.com/FaridDadashzade/deploy/main/bl_configs.json').json()

# Youtube API key
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)

# Saat & Tarix - Ölkə və Saat Dilimi
COUNTRY = str(os.environ.get("COUNTRY", ""))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# CLEAN WELCOME
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

# Last.fm modulu
BIO_PREFIX = os.environ.get("BIO_PREFIX", "@TheCyberUserBot | ")

LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    lastfm = LastFMNetwork(api_key=LASTFM_API,
                           api_secret=LASTFM_SECRET,
                           username=LASTFM_USERNAME,
                           password_hash=LASTFM_PASS)
else:
    lastfm = None

# Google Drive Modulu
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

# Genius
GENIUS = os.environ.get("GENIUS", "S2_xTvY4XdocgPC_vMSCpcjrJkA5ACbgXuUzjmWneMsWea3jCgzGem6u4mKFqG8y")
CMD_HELP = {}
CMD_HELP_BOT = {}
PM_AUTO_BAN_LIMIT = int(os.environ.get("PM_AUTO_BAN_LIMIT", 4))

SPOTIFY_DC = os.environ.get("SPOTIFY_DC", None)
SPOTIFY_KEY = os.environ.get("SPOTIFY_KEY", None)

PAKET_ISMI = os.environ.get("PAKET_ISMI", "@TheCyberUserBot Paketi")

# Avtomatik qatılma
OTOMATIK_KATILMA = sb(os.environ.get("OTOMATIK_KATILMA", "True"))

# Whitelist and Patterns /
PATTERNS = os.environ.get("PATTERNS", ".;!,")
WHITELIST = get('https://raw.githubusercontent.com/FaridDadashzade/deploy/main/whitelist.json').json()
SUPPORT = get('https://raw.githubusercontent.com/FaridDadashzade/deploy/main/support.json').json()

BLACKLIST_CHAT = os.environ.get("BLACKLIST_CHAT", None)
if not BLACKLIST_CHAT:
    BLACKLIST_CHAT = [-1001357863496]

# CloudMail.ru və MEGA.nz ayarlama
if not os.path.exists('bin'):
    os.mkdir('bin')

binaries = {
    "https://raw.githubusercontent.com/yshalsager/megadown/master/megadown":
    "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py":
    "bin/cmrudl"
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

# 'bot' dəyişgəni
if STRING_SESSION:
    # pylint: deaktiv=sehv ad
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: deaktiv=sehv ad
    bot = TelegramClient("userbot", API_KEY, API_HASH)

JARVIS = 1852686126
JARVISUSERNAME = 'fjarvisbot'

if os.path.exists("cyber.check"):
    os.remove("cyber.check")
else:
    LOGS.info("Braincheck faylı yoxdur, yüklənir...")

URL = 'https://raw.githubusercontent.com/FaridDadashzade/deploy/main/cyber.check'
with open('cyber.check', 'wb') as load:
    load.write(get(URL).content)

async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "Özəl xəta günlüyünün çalışması üçün BOTLOG_CHATID ayarlayın.")
        sys.exit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "Özəl xəta günlüyünün çalışması üçün BOTLOG_CHATID ayarlayın.")
        sys.exit(1)

    elif not BOTLOG or not LOGSPAMMER:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Hesabınızın BOTLOG_CHATID qrupuna mesaj göndərmə yetkisi yoxdur. "
            "Qrup ID'sini doğru yazıb yazmadığınızı kontrol edin.")
        sys.exit(1)
        
if not BOT_TOKEN is None:
    tgbot = TelegramClient(
        "TG_BOT_TOKEN",
        api_id=API_KEY,
        api_hash=API_HASH,
    ).start(bot_token=BOT_TOKEN)
else:
    tgbot = None


def butonlastir(sayfa, moduller):
    Satir = 5
    Kolon = 2
    
    moduller = sorted([modul for modul in moduller if not modul.startswith("_")])
    pairs = list(map(list, zip(moduller[::2], moduller[1::2])))
    if len(moduller) % 2 == 1:
        pairs.append([moduller[-1]])
    max_pages = ceil(len(pairs) / Satir)
    pairs = [pairs[i:i + Satir] for i in range(0, len(pairs), Satir)]
    butonlar = []
    for pairs in pairs[sayfa]:
        butonlar.append([
            custom.Button.inline("✅ " + pair, data=f"bilgi[{sayfa}]({pair})") for pair in pairs
        ])

    butonlar.append([custom.Button.inline("⬅️ Geri", data=f"sayfa({(max_pages - 1) if sayfa == 0 else (sayfa - 1)})"), custom.Button.inline("İrəli ➡️", data=f"sayfa({0 if sayfa == (max_pages - 1) else sayfa + 1})")])
    return [max_pages, butonlar]

with bot:
    if OTOMATIK_KATILMA:
        try:
            bot(JoinChannelRequest("@TheCyberUserBot"))
            bot(JoinChannelRequest("@TheCyberSupport"))
            bot(JoinChannelRequest("@TheCyberPlugin"))
        except:
            pass
  
    moduller = CMD_HELP
    me = bot.get_me()
    uid = me.id
    last_name = me.last_name
    first_name = me.first_name
    DEFAULT_NAME = first_name
    ISTIFADECI_ADI = me.username

    bioqrafiya = bot(GetFullUserRequest(uid))
    
    DEFAULT_BIO = bioqrafiya.full_user.about
    ALIVE_NAME = DEFAULT_NAME
    cyber_m = me.id
    SAHIB_ID = me.id
    cyber_mention = f"[{me}](tg://user?id={cyber_m})"
    
    
    try:                            
        @tgbot.on(InlineQuery)  
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query == "@TheCyberUserBot":
                rev_text = query[::-1]
                veriler = (butonlastir(0, sorted(CMD_HELP)))
                result = await builder.article(
                    f"Xahiş edirəm sadəcə .help əmrini istifadə edin.",
                    text=f"**C Y B Ξ R USERBOT**\n\n**Yüklü olan modul sayı:** `{len(CMD_HELP)}`\n**Səhifə:** 1/{veriler[0]}",
                    buttons=veriler[1],
                    link_preview=False
                )
            elif query.startswith("http"):
                parca = query.split(" ")
                result = builder.article(
                    "Fayl yükləndi",
                    text=f"**Fayl uğurla {parca[2]} saytına yükləndi!**\n\nYükləmə zamanı: {parca[1][:3]} saniyə\n[‏‏‎ ‎]({parca[0]})",
                    buttons=[
                        [custom.Button.url('URL', parca[0])]
                    ],
                    link_preview=True
                )
            else:
                result = builder.article(
                    "@TheCyberUserBot",
                    text="""@TheCyberUserBot-u işlətməyi yoxlayın!
Hesabınızı bot'a çevirə bilərsiniz və bunları istifadə edə bilərsiniz.""",
                    buttons=[
                        [custom.Button.url("Kanala Qatıl", "https://t.me/TheCyberUserBot"), custom.Button.url(
                            "Qrupa Qatıl", "https://t.me/TheCyberSupport")],
                        [custom.Button.url(
                            "GitHub", "https://github.com/FaridDadashzade/CyberUserBot")]
                    ],
                    link_preview=False
                )
            await event.answer([result] if result else None)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"sayfa\((.+?)\)")))
        async def sayfa(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarımı dəyişməyə çalışma! Özünə bir @TheCyberUserBot qur.", cache_time=0, alert=True)
            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            veriler = butonlastir(sayfa, CMD_HELP)
            await event.edit(
                f"**C Y B Ξ R USERBOT**\n\n**Yüklü olan modul sayı:** `{len(CMD_HELP)}`\n**Səhifə:** {sayfa + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"bilgi\[(\d*)\]\((.*)\)")))
        async def bilgi(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarımı dəyişməyə çalışma! Özünə bir @TheCyberUserBot qur.", cache_time=0, alert=True)

            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            komut = event.data_match.group(2).decode("UTF-8")
            try:
                butonlar = [custom.Button.inline("⚜ " + cmd[0], data=f"komut[{komut}[{sayfa}]]({cmd[0]})") for cmd in CMD_HELP_BOT[komut]['commands'].items()]
            except KeyError:
                return await event.answer("❌ Bu modula açıqlama yazılmayıb.", cache_time=0, alert=True)

            butonlar = [butonlar[i:i + 2] for i in range(0, len(butonlar), 2)]
            butonlar.append([custom.Button.inline("⬅️ Geri", data=f"sayfa({sayfa})")])
            await event.edit(
                f"**📗 Fayl:** `{komut}`\n**🔢 Əmr sayı:** `{len(CMD_HELP_BOT[komut]['commands'])}`",
                buttons=butonlar,
                link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"komut\[(.*)\[(\d*)\]\]\((.*)\)")))
        async def komut(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarımı dəyişməyə çalışma! Özünə bir @TheCyberUserBot qur.", cache_time=0, alert=True)

            cmd = event.data_match.group(1).decode("UTF-8")
            sayfa = int(event.data_match.group(2).decode("UTF-8"))
            komut = event.data_match.group(3).decode("UTF-8")

            result = f"**✅ Fayl:** `{cmd}`\n"
            if CMD_HELP_BOT[cmd]['info']['info'] == '':
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                    result += f"**⚠️ Diqqət:** {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
                else:
                    result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n\n"
            else:
                result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⚠️ Uyarı:** {CMD_HELP_BOT[cmd]['info']['warning']}\n"
                result += f"**ℹ️ Info:** {CMD_HELP_BOT[cmd]['info']['info']}\n\n"

            command = CMD_HELP_BOT[cmd]['commands'][komut]
            if command['params'] is None:
                result += f"**🛠 Əmr:** `{PATTERNS[:1]}{command['command']}`\n"
            else:
                result += f"**🛠 Əmr:** `{PATTERNS[:1]}{command['command']} {command['params']}`\n"
                
            if command['example'] is None:
                result += f"**💬 Açıqlama:** `{command['usage']}`\n\n"
            else:
                result += f"**💬 Açıqlama:** `{command['usage']}`\n"
                result += f"**⌨️ Nümunə:** `{PATTERNS[:1]}{command['example']}`\n\n"

            await event.edit(
                result,
                buttons=[custom.Button.inline("⬅️ Geri", data=f"bilgi[{sayfa}]({cmd})")],
                link_preview=False
            )
    except Exception as e:
        print(e)
        LOGS.info(
            "Botunuzda inline dəstəyi deaktivdir. "
            "Aktivləşdirmək üçün bir bot token qeyd edin və botunuzda inline modunu aktivləşdirin. "
            "Əgər bunun xaricində bir xəta olduğunu düşünürsünüzsə, bizə yazın t.me/TheCyberSupport."
        )

    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except:
        LOGS.info(
            "BOTLOG_CHATID dəyişgəni keçərli bir varlıq deyil. "
            "Ortam dəyişgənlərinizi / config.env faylınızı kontrol edin."
        )
    
from random import randint
import heroku3
heroku_api = "https://api.heroku.com"
if HEROKU_APPNAME is not None and HEROKU_APIKEY is not None:
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
    heroku_var = app.config()
else:
    app = None
     
async def cyberasistan():
    if BOT_TOKEN:
        return
    await bot.start()
    LOGS.info("C Y B Ξ R asistanı qurulur..")
    DEFAULT_NAME + "-nin asistanı"
    usnm = ISTIFADECI_ADI
    name = DEFAULT_NAME
    if usnm:
        username = usnm + "_bot"
    else:
        username = "cyber_" + (str(uid))[6:] + "_bot"
    bf = "@BotFather"
    await bot(UnblockRequest(bf))
    await bot.send_message(bf, "/cancel")
    time.sleep(3)
    await bot.send_message(bf, "/start")
    time.sleep(3)
    await bot.send_message(bf, "/newbot")
    time.sleep(3)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        LOGS.info(
            "Avtomatik bot yaratma prosesi alınmadı. @BotFather-dən manual olaraq bot yaradın."
        )
        sys.exit(1)
    await bot.send_message(bf, name)
    time.sleep(3)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await bot.send_message(bf, "My C Y B Ξ R Bot")
        time.sleep(3)
        isdone = (await bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.info(
                "Avtomatik bot yaratma prosesi alınmadı. @BotFather-dən manual olaraq bot yaradın."
            )
            sys.exit(1)
    await bot.send_message(bf, username)
    time.sleep(3)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    await bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "cyber_" + (str(uid))[7:] + str(ran) + "_bot"
        await bot.send_message(bf, username)
        time.sleep(3)
        nowdone = (await bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            await bot.send_message(bf, "/setinline")
            time.sleep(3)
            await bot.send_message(bf, f"@{username}")
            time.sleep(3)
            await bot.send_message(bf, "Search")
            time.sleep(3)
            await bot.send_message(bf, "/setabouttext")
            time.sleep(3)
            await bot.send_message(bf, f"@{username}")
            time.sleep(3)
            await bot.send_message(bf, "@TheCyberUserBot Asistan")
            time.sleep(3)
            await bot.send_message(bf, "/setuserpic")
            time.sleep(3)
            await bot.send_message(bf, f"@{username}")
            time.sleep(3)
            await bot.send_file(bf, "image/cyber.jpg")
            time.sleep(3)
            await bot.send_message(bf, "/setcommands") 
            time.sleep(3)
            await bot.send_message(bf, f"@{username}")
            time.sleep(3)
            await bot.send_message(
                bf, 
                "start - Botunuzu başladın.\
                \nhelp - Yardım menyusu\
                \nid - Bir qrup və ya istifadəçi ID almaq üçün.\
                \ntr - Tərcümə edər.\
                \ntgm - Cavab verdiyiniz medianı Telegraph'a yükləyər.\
                \ntgt - Cavab verdiyiniz mətni Telegraph'a yükləyər.\
                \npurge - Qeyd etdiyiniz mesajdan sonraki mesajları təmizləyər.\
                \ndel - Cavab verdiyiniz mesajı silər.\
                \nban - Bir istifadəçini ban etmək üçün.\
                \nunban - Bir istifadəçinin banını açar.\
                \npromote - Bir istifadəçini admin etmək üçün.\
                \ndemote - Bir istifadəçinin adminlik hüququnu almaq üçün.\
                \npin - Cavab verdiyiniz mesajı sabitləyər.",
            )
            heroku_var["BOT_TOKEN"] = token
            heroku_var["BOT_USERNAME"] = username
            LOGS.info(f"@{username} Asistanınız hazırdır.")
        else:
            LOGS.info(
                "Avtomatik bot yaratma prosesi alınmadı. @BotFather-dən manual olaraq bot yaradın."
            )
            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        await bot.send_message(bf, "/setinline")
        time.sleep(3)
        await bot.send_message(bf, f"@{username}")
        time.sleep(3)
        await bot.send_message(bf, "Search")
        time.sleep(3)
        await bot.send_message(bf, "/setabouttext")
        time.sleep(3)
        await bot.send_message(bf, f"@{username}")
        time.sleep(3)
        await bot.send_message(bf, "@TheCyberUserBot Asistan")
        time.sleep(3)
        await bot.send_message(bf, "/setuserpic")
        time.sleep(3)
        await bot.send_message(bf, f"@{username}")
        time.sleep(3)
        await bot.send_file(bf, "image/cyber.jpg") 
        time.sleep(3)
        await bot.send_message(bf, "/setcommands") 
        time.sleep(3)
        await bot.send_message(bf, f"@{username}")
        time.sleep(3)
        await bot.send_message(
            bf, 
            "start - Botunuzu başladın.\
            \nhelp - Yardım menyusu\
            \nid - Bir qrup və ya istifadəçi ID almaq üçün.\
            \ntr - Tərcümə edər.\
            \ntgm - Cavab verdiyiniz medianı Telegraph'a yükləyər.\
            \ntgt - Cavab verdiyiniz mətni Telegraph'a yükləyər.\
            \npurge - Qeyd etdiyiniz mesajdan sonraki mesajları təmizləyər.\
            \ndel - Cavab verdiyiniz mesajı silər.\
            \nban - Bir istifadəçini ban etmək üçün.\
            \nunban - Bir istifadəçinin banını açar.\
            \npromote - Bir istifadəçini admin etmək üçün.\
            \ndemote - Bir istifadəçinin adminlik hüququnu almaq üçün.\
            \npin - Cavab verdiyiniz mesajı sabitləyər.",
            )
        heroku_var["BOT_TOKEN"] = token
        heroku_var["BOT_USERNAME"] = username
        LOGS.info(f"@{username} asistanınız hazırdır.")
    else:
        LOGS.info(
            "Avtomatik bot yaratma prosesi alınmadı. @BotFather-dən manual olaraq bot yaradın."
        )
        sys.exit(1)

bot.loop.run_until_complete(cyberasistan())

# Dəyişgənlər
MYID = uid
SON_GORULME = 0
NOT_AFK = 0
COUNT_MSG = 0
USERS = {}
BRAIN_CHECKER = []
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
ISAFK = False
AFKREASON = None
ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
    [
    " ̍", " ̎", " ̄", " ̅", " ̿", " ̑", " ̆", " ̐", " ͒", " ͗",
    " ͑", " ̇", " ̈", " ̊", " ͂", " ̓", " ̈́", " ͊", " ͋", " ͌",
    " ̃", " ̂", " ̌", " ͐", " ́", " ̋", " ̏", " ̽", " ̉", " ͣ",
    " ͤ", " ͥ", " ͦ", " ͧ", " ͨ", " ͩ", " ͪ", " ͫ", " ͬ", " ͭ",
    " ͮ", " ͯ", " ̾", " ͛", " ͆", " ̚"
],
    [
    " ̕",
    " ̛",
    " ̀",
    " ́",
    " ͘",
    " ̡",
    " ̢",
    " ̧",
    " ̨",
    " ̴",
    " ̵",
    " ̶",
    " ͜",
    " ͝",
    " ͞",
    " ͟",
    " ͠",
    " ͢",
    " ̸",
    " ̷",
    " ͡",
]]
