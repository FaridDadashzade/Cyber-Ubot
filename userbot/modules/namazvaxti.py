# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

# CODER tg/@FVREED github/@FaridDadashzade #

from userbot.events import register
from requests import get 
from bs4 import BeautifulSoup
from userbot.cmdhelp import CmdHelp

@register(cyber=True, pattern=".namaz ?(.*)")
async def namaz_vaxti_scraper(event):
    seher_kodu = event.pattern_match.group(1)
    şeherler = ["Bakı", "Ağdam", "Astara", "Gəncə", "Qazax", "Quba", "Lənkəran", "Saatlı", "Sabirabad", "Şamaxı", "Şəki", "Xaçmaz", "Yevlax", "Naxçıvan", "Göyçay", "Zaqatala"]
    if seher_kodu not in şeherler:
        await event.edit("Yalnış bölgə adı qeyd etdiniz!\n\nMövcud olanlar:\n\n`Bakı, Ağdam, Astara, Gəncə, Qazax, Quba, Lənkəran, Saatlı, Sabirabad, Şamaxı, Şəki, Xaçmaz, Yevlax, Naxçıvan, Göyçay, Zaqatala`")
        return
    elif seher_kodu == 'Bakı':
        seher_kodu = 1
    elif seher_kodu == 'Ağdam':
        seher_kodu = 2
    elif seher_kodu == 'Astara':
        seher_kodu = 3
    elif seher_kodu == 'Gəncə':
        seher_kodu = 4
    elif seher_kodu == 'Qazax':
        seher_kodu = 5
    elif seher_kodu == 'Quba':
        seher_kodu = 6
    elif seher_kodu == 'Lənkəran':
        seher_kodu = 7
    elif seher_kodu == 'Saatlı':
        seher_kodu = 8 
    elif seher_kodu == 'Sabirabad':
        seher_kodu = 9
    elif seher_kodu == 'Şamaxı':
        seher_kodu = 10
    elif seher_kodu == 'Şəki':
        seher_kodu = 11
    elif seher_kodu == 'Xaçmaz':
        seher_kodu = 12
    elif seher_kodu == 'Yevlax':
        seher_kodu = 13
    elif seher_kodu == 'Naxçıvan':
        seher_kodu = 14
    elif seher_kodu == 'Göyçay':
        seher_kodu = 15
    elif seher_kodu == 'Zaqatala':
        seher_kodu = 16
    link = 'https://metbuat.az/namaz/{}/cyberuserbot.html'.format(seher_kodu)
    user_agent = "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
    request = get(link, user_agent)
    scraper = BeautifulSoup(request.content, "html.parser")
    seher_adi = scraper.find("p", {"class": 'namaz-mobile-city'}).getText()
    tarix = scraper.find("p", {"class": 'namaz-mobile-today'}).getText()
    tarix = tarix.replace(".", "/")
    subh_namazi = scraper.findAll("td")[1].getText()
    zohr_namazi = scraper.findAll("td")[5].getText() 
    esr_namazi = scraper.findAll("td")[7].getText()
    isha_namazi = scraper.findAll("td")[11].getText()
    gece_yarisi = scraper.findAll("td")[13].getText()
    msg = "🌆 **Şəhər adı:** `{}`\n📅 **Tarix:** `{}`\n\n🌅 **Sübh:** `{}`\n🏞 **Zöhr:** `{}`\n🌁 **Əsr:** `{}`\n🏙 **İşa:** `{}`\n🌃 **Gecə yarısı:** `{}`\n\n__**Powered by @TheCyberUserBot**__".format(seher_adi, tarix, subh_namazi, zohr_namazi, esr_namazi, isha_namazi, gece_yarisi)
    await event.edit(msg)

Help = CmdHelp('namaz')
Help.add_command('namaz', '<şəhər adı>', 'Seçdiyiniz şəhərə görə namaz vaxtını göstərər.', 'namaz Bakı')
Help.add_info('Şəhər adları:\nBakı, Ağdam, Astara, Gəncə, Qazax, Quba, Lənkəran, Saatlı, Sabirabad, Şamaxı, Şəki, Xaçmaz, Yevlax, Naxçıvan, Göyçay, Zaqatala')
Help.add()