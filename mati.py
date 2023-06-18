import asyncio
import logging
from telethon import types
import requests

from .. import loader, utils


logger = logging.getLogger(__name__)


@loader.tds
class YourMod(loader.Module):
    """Description for module"""  # Translateable due to @loader.tds

    strings = {
        "cfg_doc": "This is what is said, you can edit me with the configurator",
        "name": "EvilInsult",
        }

    def __init__(self):
        self.config = loader.ModuleConfig("LANG", "ru", lambda m: self.strings["cfg_doc"])

    @loader.support
    async def insultcmd(self, m: types.Message):
        """Does something when you type .example (hence, named examplecmd)"""
        args = utils.get_args(m)
        if args and args[0].isdigit():
            count = int(args[0])
        else:
            count = 1
        config = self.config["LANG"]
        url = f"https://www.evilinsult.com/generate_insult.php?lang={config}"
        tasks = []
        for _ in range(count):
            tasks.append(req(url))
        res = list(set(await asyncio.gather(*tasks)))
        await utils.answer(m, "\n".join(res))


async def req(url:str) -> str:
    return requests.get(url).text
