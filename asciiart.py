from datetime import datetime
from telethon import events
import io
import os
from PIL import Image, ImageDraw, ImageFont
import random
import math
import requests
from .. import loader, utils

def register(cb):
    cb(asciiartMod())
class asciiartMod(loader.Module):
    """Да."""
    strings = {
            "name": "asciiart",
            "no_reply": "<b>Reply to png document.</b>",
            "noimg": "<b>Там пиздец, фото нет</b>"
            }
    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self.client = client

    async def artcmd(self, message):
        """<><><<>><<<<><><>"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, self.strings("no_reply", message))

        exts = ["png"]
        if reply.file:
            if reply.file.mime_type.split("/")[1] in exts:
                await message.edit("<i>Какаю Путена ...</i>")
                BACK_COLOR = "BLACK"
                IN_IMG=await reply.download_media()
                fontik=requests.get("https://raw.githubusercontent.com/monolit/fonts/main/MiLanProVF.ttf").content
                FNT=ImageFont.truetype(io.BytesIO(fontik), 7)

                im = Image.open(IN_IMG)
                (width, height) = im.size

                line = math.ceil(im.size[0]/50 * 13 * 1.4)
                row = math.ceil(im.size[1]/50 * 6 * 1.4)

                string = ''
                for i in range(row):
                    for j in range(line):
                        string += str(random.choice([1, 0]))
                        string += '\n'

                img = Image.new('RGBA', (im.size[0], im.size[1]), BACK_COLOR)
                draw_text = ImageDraw.Draw(img)
                draw_text.text((1,1), string, spacing=1, font=FNT, fill=0)
                img2 = Image.open(IN_IMG)
                alphaComposited=Image.alpha_composite(img2, img)
                image = alphaComposited
                new_image = Image.new("RGBA", image.size, BACK_COLOR) 
                new_image.paste(image, (0, 0), image) 
                new_image.convert('RGB').save('RESULT.png', "PNG")
                await reply.reply(file='RESULT.png', force_document=True)
                os.remove(IN_IMG)
                os.remove('RESULT.png')
                await message.delete()
            else:
                await message.edit("<code> reply extension is not supportrted</code>")
        else:
            await message.edit("<code>ня, сука, ня</code>")
    async def pngcmd(self, message):
        reply = await message.get_reply_message()
        img = io.BytesIO(await reply.download_media(bytes))
        output = io.BytesIO()
        image = Image.open(img).convert("RGBA")
        ImageDraw.floodfill(image, (20000, 20000), (255, 0, 0, 0), thresh=400)
        output.name = "output.png"
        image.save(output)
        output.seek(0)
        await reply.reply(file=output, force_document=True)
