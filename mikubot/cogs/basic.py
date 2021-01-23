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

    @commands.command(
        name='bugreport',
        help='Ask the creator of Miku bot for help!',
        pass_context=True
    )
    async def support(self, ctx):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        await ctx.send('Write what issues you have, this will be sent through Miku bot to the support channel in https://discord.gg/nQ4gNCtebV')
        msg = await self.bot.wait_for('message', check=check)
        message_embed = discord.Embed(
                    color=0xE74C3C
                    )
        message_embed.set_footer(
                        text=f'Sent by {msg.author.name} at {msg.author.guild.name}',
                        icon_url=msg.author.avatar_url
                    )
        message_embed.description = msg.content
        await self.bot.get_channel(794377032464334848).send(embed=message_embed)
        await ctx.send("the message was sent successfully, If you need assistance, please join the server mentioned above. Support is offered voluntarily and nobody is forced to assist you in your perils.")
def setup(bot):
    bot.add_cog(Basic(bot))