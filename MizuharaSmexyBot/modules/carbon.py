import json
import asyncio
import requests
import aiohttp
import aiofiles
from io import BytesIO
from bs4 import BeautifulSoup
from aiohttp import ClientSession

from MizuharaSmexyBot import dispatcher
from MizuharaSmexyBot.modules.disable import DisableAbleCommandHandler

aiohttpsession = ClientSession()

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiohttpsession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image

async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply To A Text Message To Make Carbon 😆!")
    if not message.reply_to_message.text:
        return await message.reply_text(
            "Replied Message Hasn't Any Text 🤷‍♂️!"
        )
    m = await message.reply_text("`Creating Carbon ...`")
    carbon = await make_carbon(message.reply_to_message.text)
    await message.reply_photo(photo=carbon, caption='Made By @MizuharaSmexyBot Checkout @Project_Tsukiyomi')
    await m.delete()
    carbon.close()

CARBON_HANDLER = DisableAbleCommandHandler("carbon", carbon)

dispatcher.add_handler(CARBON_HANDLER)

__command_list__ = ["carbon"]
__handlers__ = [CARBON_HANDLER]
