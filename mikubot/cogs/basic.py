from discord.ext import commands
import discord

class Basic(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        name='hello',
        help='Miku says Hello!',
        pass_context=True
        )
    async def hello(self, ctx):
        await ctx.send('hello')
        return

    @commands.command(
        name='baka',
        help='Ask miku to call someone a baka!',
        pass_context=True
    )
    async def baka(self, ctx, arg):
        await ctx.send(f"{arg} is a baka!")
        return
        
def setup(bot):
    bot.add_cog(Basic(bot))