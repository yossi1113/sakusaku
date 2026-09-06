import discord
import sys
import datetime
from datetime import datetime,timezone, timedelta
from discord.ext import commands

time = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%D %H:%M:%S")

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        Pyversion = sys.version
        await ctx.reply(f"Pong! :ping_pong:\nBotのPing値は{latency}です。\n起動時間: {time}\nPythonのバージョン: {Pyversion}\n")

async def setup(bot: commands.Cog):
    await bot.add_cog(Ping(bot))