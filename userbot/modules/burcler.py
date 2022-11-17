# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

# CODER tg/@FVREED github/@FaridDadashzade#

from userbot.events import register 
from userbot.cmdhelp import CmdHelp 
from bs4 import BeautifulSoup 
from random import randint
import requests
from userbot.cmdhelp import CmdHelp

@register(cyber=True, disable_errors=True, pattern=".burc ?(.*)")
async def burcler(event):
    burc_name = event.pattern_match.group(1)
    burcler = ["qoç", "buğa", "əkizlər", "xərçəng", "şir", "qız", "tərəzi", "əqrəb", "oxatan", "oğlaq", "dolça", "balıqlar"]
    if burc_name not in burcler:
        burcler_istifade = burcler[randint(1, 12)]
        await event.edit("**Yanlış bir bürc yazdınız!**\n\n**İstifadəsi:** `.burc {}`\n\n**Bürclərin siyahısı:** `qoç, buğa, əkizlər, xərçəng, şir, qız, tərəzi, əqrəb, oxatan, oğlaq, dolça, balıqlar`".format(burcler_istifade))
        return
    elif burc_name == "qoç":
        burc_name = "qoc"
    elif burc_name == "buğa":
        burc_name == "buga"
    elif burc_name == "əkizlər":
        burc_name == "ekizler"
    elif burc_name == "xərçəng":
        burc_name == "xerceng"
    elif burc_name == "şir":
        burc_name == "sir"
    elif burc_name == "qız":
        burc_name == "qiz"
    elif burc_name == "tərəzi":
        burc_name == "terezi"
    elif burc_name == "əqrəb":
        burc_name == "eqreb"
    elif burc_name == "oxatan":
        burc_name == "oxatan"
    elif burc_name == "oğlaq":
        burc_name == "oglaq"
    elif burc_name == "dolça":
        burc_name == "dolca"
    elif burc_name == "balıqlar":
        burc_name == "baliqlar"
    burc_link = 'https://lent.az/burc/{}'.format(burc_name)
    response = requests.get(burc_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    burcler_text = soup.select('p > span')[0]
    msg = f"**Bürcünüz:** `{burc_name}`\n\n**Açıqlama:** __{burcler_text.text}__\n\n__**Powered by @TheCyberUserBot**__"
    await event.edit(msg)
    
Help = CmdHelp('burcler')
Help.add_command('burc', '<bürc-adı>', 'Gündəlik bürc məlumatları gətirər.', 'burc oxatan')
Help.add_info('Bürclər: qoç, buğa, əkizlər, xərçəng, şir, qız, tərəzi, əqrəb, oxatan, oğlaq, dolça, balıqlar')
Help.add()