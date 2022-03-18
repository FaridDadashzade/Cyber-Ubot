# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.


from telethon.tl.types import ChannelParticipantsAdmins as cp
from userbot import CMD_HELP, bot, BLACKLIST_CHAT
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from time import sleep

# ------------------------------------ #
from userbot.language import get_value
LANG = get_value("cyberlangs")
# ------------------------------------ #

dayandir = False
msjcgr = None
taglimit = 60

@register(cyber=True, pattern="^.tag(?: |$)(.*)")
async def _(q):
	global dayandir
	global msjcgr
	if q.chat_id in BLACKLIST_CHAT:
                return await q.edit(LANG["PROHIBITED_COMMAND"])
	if q.fwd_from:
		return
	if q.pattern_match.group(1):
		seasons = q.pattern_match.group(1)
	else:
		seasons = ""

	chat = await q.get_input_chat()
	a_=0
	msjcgr = True
	await q.delete()
	async for i in bot.iter_participants(chat):
		if dayandir:
			dayandir=False
			msjcgr = None
			break
		if a_ == taglimit:
			dayandir=False
			msjcgr = None
			break
		a_+=1 
		await q.client.send_message(q.chat_id, "{}\n\n[{}](tg://user?id={})".format(seasons, i.first_name, i.id))
		if taglimit <= 100:
			sleep(1)
		if taglimit > 100:
			sleep(2)


@register(cyber=True, pattern="^.alladmin(?: |$)(.*)")
async def _(q):
	global dayandir
	global msjcgr
	if q.chat_id in BLACKLIST_CHAT:
                return await q.edit(LANG["PROHIBITED_COMMAND"])
	if q.fwd_from:
		return
	if q.pattern_match.group(1):
		seasons = q.pattern_match.group(1)
	else:
		seasons = ""

	chat = await q.get_input_chat()
	a_=0
	msjcgr = True
	await q.delete()
	async for i in bot.iter_participants(chat, filter=cp):
		if dayandir:
			dayandir=False
			msjcgr = None
			break
		if a_ == taglimit:
			dayandir=False
			msjcgr = None
			break
		a_+=1
		await q.client.send_message(q.chat_id, "{}\n\n[{}](tg://user?id={})".format(seasons, i.first_name, i.id))
		if taglimit <= 100:
			sleep(1)
		if taglimit > 100:
			sleep(2)

@register(cyber=True, pattern="^.stop$")
async def _(q):
	global dayandir
	if msjcgr == None:
		await q.edit("`Siz tag prosesini başlatmamısınız.`")
		return

	dayandir = True
	await q.edit("`Tag prosesi dayandırıldı!`")
	

@register(cyber=True, pattern=".taglimit(?: |$)(.*)$")
async def _(q):
	global taglimit
	if q.pattern_match.group(1):
		pass

	else:
		return await q.edit("`Xahiş edirəm bir dəyər verin.`")

	try:
		limit=int(q.pattern_match.group(1))
	except:
		await q.edit("`Xahiş edirəm bir dəyər verin.`")
		return

	taglimit=limit
	await q.edit("`Tag etmə limitiniz {}'ə ayarlandı.`".format(str(limit)))
