import discord 
from discord.ext import *

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def setup(bot: commands.Cog):
    await bot.add_cog(Ping(bot))