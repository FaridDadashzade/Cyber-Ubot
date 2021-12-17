# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from telethon import TelegramClient
API_KEY="Bunu buraya yazın"
API_HASH="Bunu buraya yazın."
#my.telegram.org adresinden alın
bot = TelegramClient('userbot',API_KEY,API_HASH)
bot.start()
