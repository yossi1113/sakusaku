## Reload Cogs (Commands, Behavior)

import discord
from discord.ext import commands

class Reload(commands.Cog):
    def __init__(self, bot: commands.Bot):
           self.bot = bot

    @commands.command()
    @commands.is_owner() ## ボットオーナーのみ
    async def Reload(self, ctx, extension: str = None):
        print("reload going mango")
        if extension is None:
            success, mangosad = [], [] ## 成功と失敗
            for sadphonks in list(self.bot.extensions.keys()): ## sadphonks... :sob:
                try:
                    await self.bot.reload_extension(sadphonks)
                    success.append(sadphonks)
                except Exception as e: 
                    mangosad.append(f"{sadphonks}: {e}")
        else: 
            try:
                await self.bot.reload_extension(extension)
                print(f"Successfully loaded: {extension}")
            except commands.ExtensionNotLoaded: 
                print("No Load")
            except Exception as e:
                print(f"Reload Fail: {extension}: {e}")
       

async def setup(bot: commands.Cog):
    await bot.add_cog(Reload(bot))