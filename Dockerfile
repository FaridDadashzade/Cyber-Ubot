# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

FROM cyberuserbot/cyberspaceaz:dev
RUN git clone https://github.com/FaridDadashzade/Cyber-Ubot.git /root/Cyber-Ubot
WORKDIR /root/Cyber-Ubot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
