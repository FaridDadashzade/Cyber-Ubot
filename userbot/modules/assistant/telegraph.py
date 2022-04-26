# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import os
from PIL import Image
from datetime import datetime
from telegraph import Telegraph, upload_file, exceptions
from . import tgbot, DEFAULT_NAME, bot
from telethon import events
from telethon.events import *


TMP_DOWNLOAD_DIRECTORY = "./"
ad = "CyberUserBot"
telegraph = Telegraph()
r = telegraph.create_account(short_name=ad)
auth_url = r["auth_url"]

@tgbot.on(events.NewMessage(pattern="^/t(gm|gt) ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "gm":
            downloaded_file_name = await tgbot.download_media(
                r_message,
                TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            h = await event.reply("{} saniyə ərzində {} faylına endirildi.".format(downloaded_file_name, ms))
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await h.edit("Xəta: " + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await h.edit("Uğurla yükləndi.\n\nURL: https://telegra.ph{}".format(media_urls[0], (ms + ms_two)), link_preview=True)
        elif input_str == "gt":
            user_object = await tgbot.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await tgbot.download_media(
                    r_message,
                    TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(
                title_of_page,
                html_content=page_content
            )
            end = datetime.now()
            ms = (end - start).seconds
            await event.reply("Uğurla yükləndi.\n https://telegra.ph/{}".format(response["path"], ms), link_preview=True)
    else:
        await event.reply("Daimi telegra.ph linkini əldə etmək üçün bir mesaja cavab verin.")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")