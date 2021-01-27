from discord.ext import commands
import discord
import random
import datetime
import asyncio

colors = {
  'DEFAULT': 0x000000,
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'GREY': 0x95A5A6,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_GREY': 0x979C9F,
  'DARKER_GREY': 0x7F8C8D,
  'LIGHT_GREY': 0xBCC0C0,
  'DARK_NAVY': 0x2C3E50,
  'BLURPLE': 0x7289DA,
  'GREYPLE': 0x99AAB5,
  'DARK_BUT_NOT_BLACK': 0x2C2F33,
  'NOT_QUITE_BLACK': 0x23272A
}


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
    
    #embed generator
    @commands.command(
        name='embed',
        help='embeds messsage given by user',
    )
    async def embed_command(self, ctx):


        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author


        await ctx.send(content='Title?', delete_after=10)
        msg = await self.bot.wait_for('message', check=check)
        title = msg.content

        await ctx.send(content='Body?', delete_after=10)
        msg = await self.bot.wait_for('message', check=check)
        desc = msg.content

        msg = await ctx.send(content='Now generating...')
        color_list = [c for c in colors.values()]

        embed = discord.Embed(
            title=title,
            description=desc,
            color=random.choice(color_list)
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )

        await msg.edit(
            embed=embed,
            content=None
        )

        return
    #ping command
    @commands.command(
        name='ping',
        help='ping me to get the latency!',
        pass_context=True
    )
    async def ping(self, ctx):
        await ctx.send(f"Pong🏓! The ping took {round(self.bot.latency * 1000, 1)}ms!")
        return

    #autoclear command
    @commands.command(
        name='clear',
        help='deletes _ messages',
        pass_context=True
    )
    
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        deletemessage = await ctx.send(f"{amount} messages got massacred by the leek.")
        await asyncio.sleep(3)
        await deletemessage.delete()
    
    @clear.error
    async def clear_error(self, error, ctx):
        await ctx.send(error)

def setup(bot):
    bot.add_cog(Utility(bot))