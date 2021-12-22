# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from telethon import Button, custom
from userbot import *
from . import *

async def setit(cyber, ad, deyer):
    try:
        cyber.set(ad, deyer)
    except BaseException:
        return await cyber.edit("`Xəta baş verdi.`")


def geri_butonu(ad):
    button = [Button.inline("« Geri", data=f"{ad}")]
    return button