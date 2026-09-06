## Sakusaku Loader
import rich
import logging
import os
import dotenv
import asyncio
import discord
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv
from rich.logging import RichHandler

load_dotenv()

TOKEN = os.getenv("token")
Prefix = os.getenv("prefix")

Intents = discord.Intents.all()

Format = "%(message)s"
logging.basicConfig(level=logging.INFO, format=Format, datefmt="[%X]", handlers=[RichHandler()])
log = logging.getLogger("rich")

BASE_DIR = Path(__file__).parent

log.info("do a barrel roll!")

class Sakusaku(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=Prefix, intents=Intents)

    async def load_cogs(self, dir: str): ## Cogsをロード
        CogPath = BASE_DIR / dir
        for Root, dirs, file in os.walk(CogPath):
            for name in file:
                if name.endswith(".py") and not name.startswith("_"):
                    FullPath = os.path.join(Root, name)

                    ## Real Phonks Mangoss....
                    RealMangoPhonk676767676767 = os.path.relpath(FullPath,BASE_DIR)
                    extension = RealMangoPhonk676767676767.replace(os.sep, ".").removesuffix(".py")

                    try:
                        await self.load_extension(extension)
                        log.info(f"Successfully loaded: {extension}")
                    except commands.ExtensionAlreadyLoaded:
                            log.warning(f"Already loaded: {extension}")
                    except Exception as e: ## What
                            log.error(f"Failed to load {extension}: {e}")
    
    async def setup_hook(self):
        log.info("setup_hook() running")
        await self.load_cogs(dir="Cogs")

    # @is_Allowed (ホワイトリスト)
    # async def is_Allowed(userid):
    #     def 
         

    async def on_ready(self):
        log.info(f"Successfully Logged in as {self.user}!")

bot = Sakusaku()

async def Init():
    async with bot:
        await bot.start(token=TOKEN)

if __name__ == "__main__":
    asyncio.run(Init())

