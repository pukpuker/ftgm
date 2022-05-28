# requires: wget 
from .. import loader, utils
import os

def register(cb):
    cb(MSMod())

class MSMod(loader.Module):
    """Спаммер медиа"""

    strings = {
            "name": "МедиаСпам",
            "no_reply": "<b>Там пиздец, <code>reply</code> нет</b>",
            "noarg": "<i>give int count</i>"
            }

    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()

    async def podcmd(self, message):
        reply = await message.get_reply_message()
        args = utils.get_args(message)
        if not args:
            return await utils.answer(message, self.strings("noarg", message))

        count = args[0].strip()
        if not count.isdigit():
            return await utils.answer(message, self.strings("noarg", message))
        count = int(count)

        if not reply:
            return await utils.answer(message, self.strings("no_reply", message))
        if reply.media:
            await message.edit("###")
            b = await reply.download_media()
            if reply.photo:
                for _ in range(count):
                    await message.respond(file = b, reply_to = reply)
            else:
                 mess = await message.respond(file = b, reply_to = reply)
                 heshik = mess.file.id
                 for _ in range(count-1):
                     await message.respond(file = heshik, reply_to = reply)
            os.remove(b)

        if not reply.media:
            await message.edit("%%%")
            for _ in range(count):
                await message.respond(reply.text, reply_to = reply)

        await message.delete()
