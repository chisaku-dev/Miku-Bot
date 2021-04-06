from discord.ext import commands
import discord
import random
import datetime
import asyncio

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
        await ctx.send('Write what issues you have, this will be sent through Miku bot to Mori')
        msg = await self.bot.wait_for('message', check=check)
        message_embed = discord.Embed(
                    color=0xE74C3C
                    )
        message_embed.set_footer(
                        text=f'Sent by {msg.author.name} at {msg.author.guild.name}',
                        icon_url=msg.author.avatar_url
                    )
        message_embed.description = msg.content
        await self.bot.get_channel(828552431721119795).send(embed=message_embed)
        await ctx.send("the message was sent successfully")
    
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

        embed = discord.Embed(
            title=title,
            description=desc
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
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        deletemessage = await ctx.send(f"{amount} messages got massacred by the leek.", delete_after = 3)

def setup(bot):
    bot.add_cog(Utility(bot))