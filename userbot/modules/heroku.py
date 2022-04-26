# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import codecs
import heroku3
import asyncio
import aiohttp
import math
import os
import ssl
import requests
from userbot import HEROKU_APPNAME, HEROKU_APIKEY, BOTLOG, JARVIS, WHITELIST, MYID, BOTLOG_CHATID, CYBER_VERSION, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp

heroku_api = "https://api.heroku.com"
if HEROKU_APPNAME is not None and HEROKU_APIKEY is not None:
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
    heroku_var = app.config()
else:
    app = None


@register(cyber=True, pattern="^.del var ?(.*)")
async def del_var(event):
    deyer = event.pattern_match.group(1)
    if deyer == '':
        await var.edit("`Silmək istədiyiniz ConfigVars'ı seçin və mənə bildirin...`")
        return False
    await event.edit("`Məlumatları silirəm...`")
    if deyer in heroku_var:
        await event.edit("`Məlumatlar silindi!`")
        del heroku_var[deyer]
    else:
        await event.edit("`Məlumat tapılmadı!`")
        return True


@register(cyber=True, pattern=r'^.set var (\w*) ([\s\S]*)')
async def set_var(var):
    await var.edit("`Verilənlər Herokuya Yazılır...`")
    variable = var.pattern_match.group(1)
    value = var.pattern_match.group(2)
    if variable in heroku_var:
        if BOTLOG:
            await var.client.send_message(
                BOTLOG_CHATID, "#SETCONFIGVAR\n\n"
                "**ConfigVar Dəyişikliyi**:\n"
                f"`{variable}` = `{value}`"
            )
        await var.edit("`Verilənlər Herokuya Yazılır...`")
    else:
        if BOTLOG:
            await var.client.send_message(
                BOTLOG_CHATID, "#ADDCONFIGVAR\n\n"
                "**ConfigVar Əlavə**:\n"
                f"`{variable}` = `{value}`"
            )
        await var.edit("`Verilənlər əlavə edildi!`")
    heroku_var[variable] = value

    
@register(cyber=True, pattern=r"^.dyno(?: |$)")
async def dyno_usage(dyno):
    await dyno.edit("`Məlumatlar alınır...`")
    istifadeci = await bot.get_me()
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36'
                 )
    u_id = Heroku.account().id
    headers = {
     'User-Agent': useragent,
     'Authorization': f'Bearer {HEROKU_APIKEY}',
     'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + u_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("`Error: something bad happened`\n\n"
                               f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    cybergun = math.floor(hours / 24) 

    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await dyno.edit(
                "╭┈─╼━━━━━━━━━━━━━━╾─┈╮ \n"
                "│                  **CYBΞRUSERBOT DYNO**  \n"
                "├┈─╼━━━━━━━━━━━━━━╾─┈╯ \n"
                "│ Bu ay üçün istifadə etdiyiniz dyno saatı: \n"
                f"│  ▸ `{AppHours}` saat - `{AppMinutes}` dəqiqə. \n"
                f"│  ▸ Faizlə: `{AppPercentage}%` \n"
                f"│  ▸ Proqram adı: `({HEROKU_APPNAME})` \n"
                "├┈──────────────────┈╮ \n"
                "│ Bu ay üçün qalan dyno saatı: \n"
                f"│  ▸ `{hours}` saat - `{minutes}` dəqiqə. \n"
                f"│  ▸ Faizlə: `{percentage}%` \n"
                f"│  ▸ `{cybergun}` gün sonra dyno bitəcək. \n"
                "╰┈──────────────────┈╯ \n"
                f"🧞‍♂️ **Sahibim:** `{istifadeci.first_name}` \n"
            )


@register(cyber=True, pattern=r"^.hlog")  # cr: @fvreed
async def _(dyno):
    try:
        Heroku = heroku3.from_key(HEROKU_APIKEY)
        app = Heroku.app(HEROKU_APPNAME)
    except BaseException:
        return await dyno.reply(
            "`Xahiş edirəm biraz gözləyin..`"
        )
    await dyno.edit("`Log göndərilir..`")
    with open("cyberlog.txt", "w") as log:
        log.write(app.get_log())
    await dyno.client.send_file(
        dyno.chat_id,
        "cyberlog.txt",
        reply_to=dyno.id,
        caption="[C Y B Ξ R](https://t.me/TheCyberUserBot) Heroku Log.",
    )
    await dyno.delete()
    return os.remove("cyberlog.txt")


CmdHelp('heroku').add_command(
'dyno', None, 'Dyno saatı haqqında məlumat verir..'
    ).add_command(
        'set var', None, 'set var <Yeni Var adı> <Dəyər> Botunuza yeni ConfigVar əlavə edir.'
    ).add_command(
        'del var', None, 'del var <Var adı> Seçdiyiniz ConfigVarı silər.'
    ).add_command(
        'hlog', None, 'Herokudan log atar.'
    ).add()