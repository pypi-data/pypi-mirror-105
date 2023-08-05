# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import asyncio
import glob
import logging
import os
import traceback
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon import __version__ as vers
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError, PeerIdInvalidError
from telethon.tl.custom import Button
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import InputMessagesFilterDocument

from . import *
from .functions.all import AreUpdatesAvailable
from .utils import *
from .version import __version__ as ver

# remove the old logs file.
if os.path.exists("ultroid.log"):
    os.remove("ultroid.log")

# start logging into a new file.
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("ultroid.log"), logging.StreamHandler()],
)

if not os.path.isdir("resources/auths"):
    os.mkdir("resources/auths")

if not os.path.isdir("resources/downloads"):
    os.mkdir("resources/downloads")

if not os.path.isdir("addons"):
    os.mkdir("addons")

token = udB.get("GDRIVE_TOKEN")
if token:
    with open("resources/auths/auth_token.txt", "w") as t_file:
        t_file.write(token)

websocket = udB.get("WEBSOCKET_URL")
if websocket:
    ulr = f"WEBSOCKET_URL={websocket}"
    with open(".env", "w") as t:
        t.write(ulr)


async def istart(ult):
    await ultroid_bot.start(ult)
    ultroid_bot.me = await ultroid_bot.get_me()
    ultroid_bot.uid = telethon.utils.get_peer_id(ultroid_bot.me)
    ultroid_bot.first_name = ultroid_bot.me.first_name
    if not ultroid_bot.me.bot:
        udB.set("OWNER_ID", ultroid_bot.uid)
    if str(BOT_MODE) == "True":
        OWNER = await ultroid_bot.get_entity(int(udB.get("OWNER_ID")))
        ultroid_bot.me = OWNER
        asst.me = OWNER
        ultroid_bot.uid = OWNER.id
        ultroid_bot.first_name = OWNER.first_name


ultroid_bot.asst = None


async def bot_info(botasst):
    await botasst.start()
    botasst.me = await botasst.get_me()
    return botasst.me


LOGS.info(
    """
                -----------------------------------
                        Starting Deployment
                -----------------------------------
"""
)


LOGS.info("Initialising...")
LOGS.info(f"py-Ultroid Version - {ver}")
LOGS.info(f"Telethon Version - {vers}")
LOGS.info("Ultroid Version - 0.0.6")

if str(BOT_MODE) == "True":
    mode = "Bot Mode - Started"
else:
    mode = "User Mode - Started"

# log in
if Var.BOT_TOKEN:
    LOGS.info("Starting Ultroid...")
    try:
        ultroid_bot.asst = TelegramClient(
            None, api_id=Var.API_ID, api_hash=Var.API_HASH
        ).start(bot_token=Var.BOT_TOKEN)
        asst = ultroid_bot.asst
        ultroid_bot.loop.run_until_complete(istart(asst))
        ultroid_bot.loop.run_until_complete(bot_info(asst))
        LOGS.info("Done, startup completed")
        LOGS.info(mode)
    except AuthKeyDuplicatedError:
        LOGS.info(
            "Session String expired. Please create a new one! Ultroid is stopping..."
        )
        exit(1)
    except BaseException:
        LOGS.info("Error: " + str(traceback.print_exc()))
        exit(1)
else:
    LOGS.info(mode)
    ultroid_bot.start()

BOTINVALID_PLUGINS = [
    "globaltools",
    "autopic",
    "pmpermit",
    "fedutils",
    "_tagnotifs",
    "webupload",
    "clone",
    "inlinefun",
    "tscan",
    "animedb",
    "limited",
    "quotly",
    "findsong",
    "sticklet",
]

# for userbot
path = "plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        try:
            if str(BOT_MODE) == "True" and plugin_name in BOTINVALID_PLUGINS:
                LOGS.info(
                    f"Ultroid - Official - BOT_MODE_INVALID_PLUGIN - {plugin_name}"
                )
            else:
                load_plugins(plugin_name.replace(".py", ""))
                if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                    LOGS.info(f"Ultroid - Official -  Installed - {plugin_name}")
        except Exception as e:
            LOGS.info(f"Ultroid - Official - ERROR - {plugin_name}")
            LOGS.info(str(e))


# for addons
addons = udB.get("ADDONS")
if addons == "True" or addons is None:
    try:
        os.system("git clone https://github.com/TeamUltroid/UltroidAddons.git addons/")
    except BaseException:
        pass
    LOGS.info("Installing packages for addons")
    os.system("pip install -r addons/addons.txt")
    path = "addons/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            try:
                if str(BOT_MODE) == "True" and plugin_name in BOTINVALID_PLUGINS:
                    LOGS.info(
                        f"Ultroid - Addons - BOT_MODE_INVALID_PLUGIN - {plugin_name}"
                    )
                else:
                    load_addons(plugin_name.replace(".py", ""))
                    if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                        LOGS.info(f"Ultroid - Addons - Installed - {plugin_name}")
            except Exception as e:
                LOGS.warning(f"Ultroid - Addons - ERROR - {plugin_name}")
                LOGS.warning(str(e))
else:
    os.system("cp plugins/__init__.py addons/")


# for assistant
path = "assistant/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        try:
            load_assistant(plugin_name.replace(".py", ""))
            if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                LOGS.info(f"Ultroid - Assistant - Installed - {plugin_name}")
        except Exception as e:
            LOGS.warning(f"Ultroid - Assistant - ERROR - {plugin_name}")
            LOGS.warning(str(e))

# for channel plugin
Plug_channel = udB.get("PLUGIN_CHANNEL")
if Plug_channel:

    async def plug():
        if str(BOT_MODE) == "True":
            LOGS.info("PLUGIN_CHANNEL Can't be used in BOT_MODE")
            return
        try:
            try:
                if not Plug_channel.startswith("/"):
                    chat = int(Plug_channel)
                else:
                    return
            except BaseException:
                if Plug_channel.startswith("@"):
                    chat = Plug_channel
                else:
                    return
            plugins = await ultroid_bot.get_messages(
                chat,
                None,
                search=".py",
                filter=InputMessagesFilterDocument,
            )
            total = int(plugins.total)
            totals = range(0, total)
            for ult in totals:
                uid = plugins[ult].id
                file = await ultroid_bot.download_media(
                    await ultroid_bot.get_messages(chat, ids=uid), "./addons/"
                )
                if "(" not in file:
                    upath = Path(file)
                    name = upath.stem
                    try:
                        load_addons(name.replace(".py", ""))
                        LOGS.info(
                            f"Ultroid - PLUGIN_CHANNEL - Installed - {(os.path.basename(file))}"
                        )
                    except Exception as e:
                        LOGS.warning(
                            f"Ultroid - PLUGIN_CHANNEL - ERROR - {(os.path.basename(file))}"
                        )
                        LOGS.warning(str(e))
                else:
                    LOGS.info(f"Plugin {(os.path.basename(file))} is Pre Installed")
                    os.remove(file)
        except Exception as e:
            LOGS.warning(str(e))


# chat via assistant
pmbot = udB.get("PMBOT")
if pmbot == "True":
    path = "assistant/pmbot/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            load_pmbot(plugin_name.replace(".py", ""))
    LOGS.info(f"Ultroid - PM Bot Message Forwards - Enabled.")

# customize assistant


async def semxy():
    try:
        xx = await ultroid_bot.get_entity(asst.me.username)
        if xx.photo is None:
            LOGS.info("Customising Ur Assistant Bot in @BOTFATHER")
            UL = f"@{asst.me.username}"
            if (ultroid_bot.me.username) is None:
                sir = ultroid_bot.me.first_name
            else:
                sir = f"@{ultroid_bot.me.username}"
            await ultroid_bot.send_message(
                Var.LOG_CHANNEL, "Auto Customisation Started on @botfather"
            )
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/cancel")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/start")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/setuserpic")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_file(
                "botfather", "resources/extras/ultroid_assistant.jpg"
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/setabouttext")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                "botfather", f"✨Hello✨!! I'm Assistant Bot of {sir}"
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/setdescription")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                "botfather",
                f"✨PowerFull Ultroid Assistant Bot✨\n✨Master ~ {sir} ✨\n\n✨Powered By ~ @TeamUltroid✨",
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/start")
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                Var.LOG_CHANNEL, "**Auto Customisation** Done at @BotFather"
            )
            LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.warning(str(e))


# some stuffs
async def hehe():
    if Var.LOG_CHANNEL:
        try:
            try:
                await ultroid_bot(
                    AddChatUserRequest(
                        chat_id=Var.LOG_CHANNEL,
                        user_id=asst.me.username,
                        fwd_limit=10,
                    ),
                )
            except BaseException:
                try:
                    await ultroid_bot(
                        InviteToChannelRequest(
                            channel=Var.LOG_CHANNEL, users=[asst.me.username]
                        )
                    )
                except PeerIdInvalidError:
                    LOGS.warning("WRONG CHANNEL/GROUP ID in LOG_CHANNEL Var")
                except BaseException as ep:
                    LOGS.info(ep)
            MSG = f"**Ultroid has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.me.id})\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖\n**Support**: @TeamUltroid\n➖➖➖➖➖➖➖➖➖"
            BTTS = None
            updava = await AreUpdatesAvailable()
            if updava:
                BTTS = [[Button.inline(text="Update Available", data="updtavail")]]
            await ultroid_bot.asst.send_message(Var.LOG_CHANNEL, MSG, buttons=BTTS)
        except BaseException:
            try:
                MSG = f"**Ultroid has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.me.id})\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖\n**Support**: @TeamUltroid\n➖➖➖➖➖➖➖➖➖"
                await ultroid_bot.send_message(Var.LOG_CHANNEL, MSG)
            except PeerIdInvalidError:
                LOGS.warning("WRONG CHANNEL/GROUP ID in LOG_CHANNEL Var")
            except BaseException as ef:
                LOGS.info(ef)
    try:
        await ultroid_bot(JoinChannelRequest("@TheUltroid"))
    except BaseException:
        pass


if str(BOT_MODE) != "True":
    ultroid_bot.loop.run_until_complete(semxy())
    if Plug_channel:
        ultroid_bot.loop.run_until_complete(plug())
ultroid_bot.loop.run_until_complete(hehe())

LOGS.info(
    """
                ----------------------------------------------------------------------
                    Ultroid has been deployed! Visit @TheUltroid for updates!!
                ----------------------------------------------------------------------
"""
)

if __name__ == "__main__":
    ultroid_bot.run_until_disconnected()
