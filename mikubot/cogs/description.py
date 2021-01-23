from discord.ext import commands
import discord

class AnnouncementsInfo(commands.Cog, name="Announcements and Bot Info!"):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        name='info',
        help="Hey guys, I'm the creator of Miku bot. I hope you have a good time playing with Miku! Be sure to make a #global channel in your server to join the cross server chatroom! You can join our support server at https://discord.gg/nQ4gNCtebV or find any of my accounts through https://sites.google.com/view/anivocaloid/link-redirection!",
        pass_context=True
        )
    async def support(self, ctx):
        info_embed = discord.Embed()
        info_embed.title='Bot Info'
        info_embed.description='Hey guys, I\'m the creator of Miku bot. I hope you have a good time playing with Miku! Be sure to make a #global channel in your server to join the cross server chatroom! You can join our support server at https://discord.gg/nQ4gNCtebV or find any of my accounts through https://sites.google.com/view/anivocaloid/link-redirection!'
        info_embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed = info_embed)
        return

def setup(bot):
    bot.add_cog(AnnouncementsInfo(bot))