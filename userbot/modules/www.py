# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from datetime import datetime
import speedtest
from telethon import functions
from userbot import CMD_HELP, JARVIS, MYID
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("www")

# ████████████████████████████████ #

def convert(speed):
    return round(int(speed) / 1048576, 2)

@register(outgoing=True, pattern="^.speed$")
async def speedtst(spd):
    await spd.edit(LANG['SPEED'])
    speed = speedtest.Speedtest()

    speed.get_best_server()
    speed.download()
    speed.upload()
    result = speed.results.dict()

    await spd.edit("`"
                   f"{LANG['STARTED_TIME']}"
                   f"{result['timestamp']} \n\n"
                   f"{LANG['DOWNLOAD_SPEED']}"
                   f"{convert(result['download'])} \n"
                   f"{LANG['UPLOAD_SPEED']}"
                   f"{convert(result['upload'])} \n"
                   "Ping: "
                   f"{result['ping']} \n"
                   f"{LANG['ISP']}"
                   f"{result['client']['isp']}"
                   "`")


def speed_convert(size):
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern="^.dc$")
async def neardc(event):
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(f"Şəhər: `{result.country}`\n"
                     f"Ən yaxın datacenter : `{result.nearest_dc}`\n"
                     f"Hal-hazırki datacenter : `{result.this_dc}`")


@register(outgoing=True, pattern="^.ping$")
async def pingme(pong):
    start = datetime.now()
    await pong.edit("`Pong!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit("`Pong!\n%sms`" % (duration))


CmdHelp('www').add_command(
    'speed', None, 'Bir speedtest nəticəsi göstərər.'
).add_command(
    'dc', None, 'Serverinizə ən yaxın datacenter\'ı göstərər.'
).add_command(
    'ping', None, 'Botun ping dəyərini göstərər.'
).add()
