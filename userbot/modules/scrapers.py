# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import os
import time
import requests
import asyncio
import shutil
from bs4 import BeautifulSoup
from bing_image_downloader import downloader
from shutil import rmtree
import re
from PIL import Image
from time import sleep
from html import unescape
from re import findall
from selenium import webdriver
from urllib.parse import quote_plus
from urllib.error import HTTPError
from google_trans_new import LANGUAGES, google_translator
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
from requests import get
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from gtts.lang import tts_langs
from emoji import get_emoji_regexp
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from asyncio import sleep
from userbot import CMD_HELP, BOTLOG, bot, BOTLOG_CHATID, YOUTUBE_API_KEY, CHROME_DRIVER, GOOGLE_CHROME_BIN
from userbot.events import register
from userbot.modules.upload_download import progress, humanbytes, time_formatter
from ImageDown import ImageDown
import base64, binascii
import random
from userbot.cmdhelp import CmdHelp
from userbot.utils import chrome, progress
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeAudio
from telethon import events
from userbot import LANGUAGE as DIL

CARBONLANG = "auto"
TTS_LANG = "tr"
TRT_LANG = DIL

from telethon import events
import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import glob

@register(outgoing=True, pattern="^.crblang (.*)")
async def setlang(prog):
    global CARBONLANG
    CARBONLANG = prog.pattern_match.group(1)
    await prog.edit(f"Karbon modulu üçün default dil {CARBONLANG} olaraq ayarlandı.")

@register(outgoing=True, pattern="^.carbon")
async def carbon_api(e):
    await e.edit("`Hazırlanır...`")
    CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
    global CARBONLANG
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)
    code = quote_plus(pcode) 
    await e.edit("`Hazırlanır...\nFaiz: 25%`")
    if os.path.isfile("./carbon.png"):
        os.remove("./carbon.png")
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    await e.edit("`Hazırlanır...\nFaiz: 50%`")
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_path
        }
    }
    command_result = driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    await e.edit("`Hazırlanır...\nFaiz: 75%`")
    while not os.path.isfile("./carbon.png"):
        await sleep(0.5)
    await e.edit("`Hazırlanır...\nFaiz: 100%`")
    file = './carbon.png'
    await e.edit("`Foto hazırlanır...`")
    await e.client.send_file(
        e.chat_id,
        file,
        caption="Bu şəkil [Carbon](https://carbon.now.sh/about/) istifadə edilərək hazırlandı,\
        \nbir [Dawn Labs](https://dawnlabs.io/) proyektidir.",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )

    os.remove('./carbon.png')
    driver.quit()
    await e.delete()

@register(outgoing=True, pattern="^.currency ?(.*)")
async def moni(event):
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(" ")
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = "https://api.exchangeratesapi.io/latest?base={}".format(
                currency_from)
            current_response = get(request_url).json()
            if currency_to in current_response["rates"]:
                current_rate = float(current_response["rates"][currency_to])
                rebmun = round(number * current_rate, 2)
                await event.edit("{} {} = {} {}".format(
                    number, currency_from, rebmun, currency_to))
            else:
                await event.edit(
                    "`Bir xəta baş verdi...`"
                )
        except Exception as e:
            await event.edit(str(e))
    else:
        await event.edit("`Yanlış sintaksis.`")
        return

# The codes belong entirely to https://github.com/FaridDadashzade. Reuse is not allowed.
# © https://t.me/FVREED 
      
@register(cyber=True, pattern=r"^.google ?(.*)")
async def googlesearch(cyber):
    soz = cyber.pattern_match.group(1)
    sehife = 1  
    start = (sehife - 1) * 10 + 1
    if not soz:
        await cyber.edit("`Axtarış edə bilməyim üçün mənə birşey verin!`")
        return
    CYBER_API_KEY = ('AIzaSyC3psXHEJpBHuNXdWUMBuU6QmTam0YXwRg')
    url = f"https://www.googleapis.com/customsearch/v1?key={CYBER_API_KEY}&cx=003124365989545633216:m49jkqxkn0e&q={soz}&start={start}"
    data = requests.get(url).json()
    axtaris = data.get("items")
    alinan_neticeler = ""
    for i, sozu_axtar in enumerate(axtaris, start=1):
        basliq = sozu_axtar.get("title")
        sayt_aciqlamasi = sozu_axtar.get("htmlSnippet")
        link = sozu_axtar.get("link")
        alinan_neticeler += f"<b>{basliq}</b>\n<i>{sayt_aciqlamasi}</i>\n\n{link}\n\n"
    try:
        await cyber.edit("<b>Axtardığınız:</b>\n<i>" + soz + "</i>\n\n<b>Nəticə:</b>\n" +
                       alinan_neticeler,
                       link_preview=False, parse_mode="html")
    except UnboundLocalError:
        pass
    if BOTLOG:
        await cyber.client.send_message(
            BOTLOG_CHATID,
            soz + "`sözü Google'da axtarıldı!`",
        )
        
# The codes belong entirely to https://github.com/FaridDadashzade. Reuse is not allowed.
# © https://t.me/FVREED 

@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Xəta.\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Axtardığınız səhifə tapılmadı.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open("wiki.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "wiki.txt",
            reply_to=wiki_q.id,
            caption="`Nəticə çox uzundur, fayl olaraq göndərirəm...`",
        )
        if os.path.exists("wiki.txt"):
            os.remove("wiki.txt")
        return
    await wiki_q.edit("**Axtarış:**\n`" + match + "`\n\n**Nəticə:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"{match}` teriminin Wikipedia sorğusu uğurla hazırlandı!`")


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(event):
    if event.fwd_from:
        return
    ttss = event.pattern_match.group(1)
    rep_msg = None
    if event.is_reply:
        rep_msg = await event.get_reply_message()
    if len(ttss) < 1:
        if event.is_reply:
            sarki = rep_msg.text
        else:
            await event.edit("`Səsə çevirməyim üçün əmrin yanında bir mesaj yazmalısınız.`")
            return

    await event.edit(f"__Səsə çevirilir...__")
    chat = "@MrTTSbot"
    async with bot.conversation(chat) as conv:
        try:     
            await conv.send_message(f"/tomp3 {ttss}")
        except YouBlockedUserError:
            await event.reply(f"`Hmm deyəsən` {chat} `əngəlləmisən. Xahiş edirəm bloku aç.`")
            return
        ses = await conv.wait_event(events.NewMessage(incoming=True,from_users=1678833172))
        await event.client.send_read_acknowledge(conv.chat_id)
        indir = await ses.download_media()
        voice = await asyncio.create_subprocess_shell(f"ffmpeg -i '{indir}' -c:a libopus 'MrTTSbot.ogg'")
        await voice.communicate()
        if os.path.isfile("MrTTSbot.ogg"):
            await event.client.send_file(event.chat_id, file="MrTTSbot.ogg", voice_note=True, reply_to=rep_msg)
            await event.delete()
            os.remove("MrTTSbot.ogg")
        else:
            await event.edit("`Bir xəta baş verdi!`")


        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "Uğurla səsə çevirildi!")
        
@register(outgoing=True, pattern="^.imdb (.*)")
async def imdb(e):
    try:
        movie_name = e.pattern_match.group(1)
        remove_space = movie_name.split(' ')
        final_name = '+'.join(remove_space)
        page = get("https://www.imdb.com/find?ref_=nv_sr_fn&q=" + final_name +
                   "&s=all")
        lnk = str(page.status_code)
        soup = BeautifulSoup(page.content, 'lxml')
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext('td').findNext('td').text
        mov_link = "http://www.imdb.com/" + \
            odds[0].findNext('td').findNext('td').a['href']
        page1 = get(mov_link)
        soup = BeautifulSoup(page1.content, 'lxml')
        if soup.find('div', 'poster'):
            poster = soup.find('div', 'poster').img['src']
        else:
            poster = ''
        if soup.find('div', 'title_wrapper'):
            pg = soup.find('div', 'title_wrapper').findNext('div').text
            mov_details = re.sub(r'\s+', ' ', pg)
        else:
            mov_details = ''
        credits = soup.findAll('div', 'credit_summary_item')
        if len(credits) == 1:
            director = credits[0].a.text
            writer = 'Not available'
            stars = 'Not available'
        elif len(credits) > 2:
            director = credits[0].a.text
            writer = credits[1].a.text
            actors = []
            for x in credits[2].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        else:
            director = credits[0].a.text
            writer = 'Not available'
            actors = []
            for x in credits[1].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        if soup.find('div', "inline canwrap"):
            story_line = soup.find('div',
                                   "inline canwrap").findAll('p')[0].text
        else:
            story_line = 'Not available'
        info = soup.findAll('div', "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll('a')
                for i in a:
                    if "country_of_origin" in i['href']:
                        mov_country.append(i.text)
                    elif "primary_language" in i['href']:
                        mov_language.append(i.text)
        if soup.findAll('div', "ratingValue"):
            for r in soup.findAll('div', "ratingValue"):
                mov_rating = r.strong['title']
        else:
            mov_rating = 'Not available'
        await e.edit('<a href=' + poster + '>&#8203;</a>'
                     '<b>Başlıq : </b><code>' + mov_title + '</code>\n<code>' +
                     mov_details + '</code>\n<b>Reytinq : </b><code>' +
                     mov_rating + '</code>\n<b>Ölkə : </b><code>' +
                     mov_country[0] + '</code>\n<b>Dil : </b><code>' +
                     mov_language[0] + '</code>\n<b>Rejissor : </b><code>' +
                     director + '</code>\n<b>Yazar : </b><code>' + writer +
                     '</code>\n<b>Ulduzlar : </b><code>' + stars +
                     '</code>\n<b>IMDB Url : </b>' + mov_link +
                     '\n<b>Hekayə : </b>' + story_line,
                     link_preview=True,
                     parse_mode='HTML')
    except IndexError:
        await e.edit("Düzgün bir film adı qeyd edin.")


@register(outgoing=True, pattern=r"^.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """.trt"""
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Tərcümə edə bilməyim üçün mənə bir mətn ver!`")
        return

    try:
        reply_text = translator.translate(deEmojify(message), dest=TRT_LANG)
    except ValueError:
        await trans.edit("Səhv dil kodu.")
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = f"Bu dildən: **{source_lan.title()}**\nBu dilə: **{transl_lan.title()}**\n\n{reply_text.text}"

    await trans.edit(reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"{source_lan.title()} sözü {transl_lan.title()} tərcümə edildi.",
        )

        
@register(pattern=".lang (trt|tts) (.*)", outgoing=True)
async def lang(value):
    util = value.pattern_match.group(1).lower()
    if util == "trt":
        scraper = "Translator"
        global TRT_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            await value.edit(
                f"`Səhv dil kodu!`\n`Dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    elif util == "tts":
        scraper = "Yazıdan Sese"
        global TTS_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            await value.edit(
                f"`Səhv dil kodu!`\n`Dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    await value.edit(f"`{scraper} modulu üçün default dil {LANG.title()} dilinə çevirildi.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID,
            f"`{scraper} modulu üçün default dil {LANG.title()} dilinə çevirildi.`")

        
@register(outgoing=True, pattern="^.yt (.*)")
async def _(event):
    try:
      from youtube_search import YoutubeSearch
    except:
      os.system("pip install youtube_search")
    from youtube_search import YoutubeSearch
    if event.fwd_from:
        return
    fin = event.pattern_match.group(1)
    stark_result = await event.edit("`Axtarılır...`")
    results = YoutubeSearch(f"{fin}", max_results=5).to_dict()
    noob = "<b>YOUTUBE AXTARIŞI</b> \n\n"
    for moon in results:
      ytsorgusu = moon["id"]
      kek = f"https://www.youtube.com/watch?v={ytsorgusu}"
      stark_name = moon["title"]
      stark_chnnl = moon["channel"]
      total_stark = moon["duration"]
      stark_views = moon["views"]
      noob += (
        f"<b><u>Ad</u></b> ➠ <code>{stark_name}</code> \n"
        f"<b><u>Link</u></b> ➠  {kek} \n"
        f"<b><u>Kanal</u></b> ➠ <code>{stark_chnnl}</code> \n"
        f"<b><u>Video Uzunluğu</u></b> ➠ <code>{total_stark}</code> \n"
        f"<b><u>Görüntülənmə</u></b> ➠ <code>{stark_views}</code> \n\n"
        )
      await stark_result.edit(noob, parse_mode="HTML")

@register(outgoing=True, pattern=r".rip(a|v) (.*)")
async def download_video(v_url):
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    await v_url.edit("`Yüklənməyə hazırlanır...`")

    if type == "a":
        opts = {
            'format':
            'bestaudio',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'writethumbnail':
            True,
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
            '%(id)s.mp3',
            'quiet':
            True,
            'logtostderr':
            False
        }
        video = False
        song = True

    elif type == "v":
        opts = {
            'format':
            'best',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
            '%(id)s.mp4',
            'logtostderr':
            False,
            'quiet':
            True
        }
        song = False
        video = True

    try:
        await v_url.edit("`Lazımi məlumatlar yüklənir...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("`Yüklənəcək video çox qısadır.`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Malesef coğrafi kısıtlamalar yüzünden işlem yapamazsın`")
        return
    except MaxDownloadsReached:
        await v_url.edit("`Maksimum yüklenme limiti aşıldı.`")
        return
    except PostProcessingError:
        await v_url.edit("`İstek sırasında bir hata baş verdi.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Error UnavialableVideoError |//\\| Bu mesajı görürsen büyük ihtimal ile userbotunda _youtube_ modulu xəta verdi bu mesajı @TheCyberSupport qrupuna göndər`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`Bir xəta baş verdi.`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Musiqi yüklənməyə hazırlanır:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(rip_data['duration']),
                                       title=str(rip_data['title']),
                                       performer=str(rip_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Hazırlanır...",
                         f"{rip_data['title']}.mp3")))
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await v_url.edit(f"`Musiqi yüklənməyə hazırlanır:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Hazırlanır...",
                         f"{rip_data['title']}.mp4")))
        os.remove(f"{rip_data['id']}.mp4")
        await v_url.delete()

@register(cyber=True, pattern="^.img ?(.*)")
async def sekil_axtar(event):
    axtaris_name = event.pattern_match.group(1)
    if not axtaris_name:
        await event.edit("`Axtarış edə bilməyim üçün bir ad qeyd edin.`")
        return

    axtaris = f'"{axtaris_name}"'
    axtarilir = await event.edit("`{}` üçün şəkil axtarılır..".format(axtaris_name))
    downloader.download(axtaris, limit=5,  output_dir='sekil_axtaris', adult_filter_off=True, force_replace=False, timeout=5, verbose=True)
    os.chdir(f'./sekil_axtaris/{axtaris}')
    toplam_fayl = []
    fayl_tipleri = ("*.png", "*.jpeg", "*.jpg")
    for fayllar in fayl_tipleri:
        toplam_fayl.extend(glob.glob(fayllar))
    try:
        await event.client.send_file(event.chat_id, toplam_fayl, caption="**Powered by @TheCyberUserBot**")
        await axtarilir.delete()
    except:
        await event.edit("**Şəkil tapılmadı!**")
    os.chdir('/root/CyberUserBot')
    os.system("rm -rf sekil_axtaris")               

def deEmojify(inputString):
    return get_emoji_regexp().sub(u'', inputString)

CmdHelp('scrapers').add_command(
    'currency', '<miqdar> <vahid>', '<çevriləcək vahid>', 'Valyuta.'
).add_command(
    'carbon', '<mətn>', 'carbon.now.sh saytından istifadə edərək mesajınıza carbon effekti verər.'
).add_command(
    'crblang', '<dil>', 'Carbon üçün dil ayarlayar.'
).add_command(
    'google', '<söz>', 'Googleda axtarış etmənizə yardım edəcək modul.'
).add_command(
    'img', '<söz>', 'Googledən yazdığınız sözə uyğun şəkillər əldə edin.'
).add_command(
    'wiki', '<term>', 'Wikipedia-da axtarış edər.'
).add_command(
    'tts', '<mətn>', 'Mətni səsə çevirər.'
).add_command(
    'lang', '<dil>', 'tts vƏ trt üçün dil ayarlayın.'
).add_command(
    'trt', '<mətn>', 'Tərcümə edin!'
).add_command(
    'yt', '<mətn>', 'YouTube-da axtarış edər'
).add_command(
    'imdb', '<film>', 'Film haqqında məlumat verər verir.'
).add_command(
    'ripa', '<link>', 'YouTube-dan (və ya başqa saytlardan) səs yükləyər.'
).add_command(
    'ripv', '<link>', 'YouTube-dan (və ya başqa saytlardan) video yükləyər.'
).add_info(
    '[Rip əmrinin dəstəkləndiyi saytlar.](https://ytdl-org.github.io/youtube-dl/supportedsites.html)'
).add()
