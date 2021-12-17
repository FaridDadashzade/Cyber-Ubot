from covid import Covid
from userbot.cmdhelp import CmdHelp 
from userbot.events import register


@register(cyber=True, pattern="^.covid (.*)")
async def corona(event):
    await event.edit("`Məlumatlar alınır...`")
    country = event.pattern_match.group(1)
    if not country:
        await event.edit("İstifadəsi: `.covid <ölkə adı>`\nNümunə: `.covid Azerbaijan`")
        return
    covid = Covid(source="worldometers")
    country_data = covid.get_status_by_country_name(country)
    if country_data:
        output_text = f"`⚠️ Aşkarlandı : {country_data['confirmed']} (+{country_data['new_cases']})`\n"
        output_text += f"`☢️ Aktiv: {country_data['active']}`\n"
        output_text += f"`🤕 Kritik: {country_data['critical']}`\n"
        output_text += f"`😟 Yeni ölüm sayı: {country_data['new_deaths']}`\n\n"
        output_text += f"`⚰️ Ümumi ölüm sayı: {country_data['deaths']} (+{country_data['new_deaths']})`\n"
        output_text += f"`😔 Yeni yoluxma: {country_data['new_cases']}`\n"
        output_text += f"`😇 Sağalan: {country_data['recovered']}`\n"
        output_text += f"Bu məlumatlar [Worldometer](https://www.worldometers.info/coronavirus/country/{country}) saytından alınır."
    else:
        output_text = "Bu ölkə üçün heç bir məlumat tapılmadı!"

    await event.edit(f"`{country} üçün məlumatlar:`\n\n{output_text}")


Help = CmdHelp('covid')
Help.add_command('covid', '<ölkə adı>', 'Worldometer saytından qeyd etdiyiniz ölkə üçün korona virus məlumatlarını gətirər.')
Help.add()
