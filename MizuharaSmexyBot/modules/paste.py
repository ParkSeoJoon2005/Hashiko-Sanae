import os
import re

import aiofiles
from pyrogram import filters

from MizuharaSmexyBot import dispatcher
from MizuharaSmexyBot.core.decorators.errors import capture_err
from MizuharaSmexyBot.core.keyboard import ikb
from MizuharaSmexyBot.utils.pastebin import paste
from MizuharaSmexyBot.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async


PASTE_HANDLER = DisableAbleCommandHandler("paste", paste)
dispatcher.add_handler(PASTE_HANDLER)

__mod_name__ = "Paste"
__command_list__ = ["Paste"]
__handlers__ = [PASTE_HANDLER]
__help__ = "/paste - To Paste Replied Text Or Document To A Pastebin"
pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


@run_async(filters.command("paste") & ~filters.edited)
async def paste_func(_, message):
    if not message.reply_to_message:
        return await message.reply("Reply To A Message With /paste")
    r = message.reply_to_message

    if not r.text and not r.document:
        return await message.reply("Only text and documents are supported.")

    m = await message.reply("Pasting...")

    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await m.edit("You can only paste files smaller than 40KB.")
        if not pattern.search(r.document.mime_type):
            return await m.edit("Only text files can be pasted.")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)

    link = await paste(content)
    kb = ikb({"Paste Link": link})
    try:
        await message.reply_photo(photo=link, quote=False, reply_markup=kb)
    except Exception:
        await message.reply("Here's your paste", reply_markup=kb)
    await m.delete()
