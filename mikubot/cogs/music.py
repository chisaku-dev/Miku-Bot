import asyncio
from os import name

import discord
import youtube_dl

from youtube_search import YoutubeSearch

from discord.ext import commands
from discord import FFmpegPCMAudio

import re
from pytube import Playlist
import random

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="play",
        help="Miku searches then adds link to queue for playing!"
    )
    async def play(self, ctx, *, search: str):
        try:
            if not ctx.voice_client.is_playing():
                global queue
                queue = []
        except:
            return
        if not 'https' in search:
            results = YoutubeSearch(search, max_results=1).to_dict()
            urlsuffix = results[0].get('url_suffix')
            url = ('https://www.youtube.com' +urlsuffix)
            await ctx.send('Added to queue: {}'.format(results[0].get('title')), delete_after=5)
            queue.append(url)
        elif 'playlist?' in search:
            playlist = Playlist(search)
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            counter = 0
            for url in playlist.video_urls:
                counter = counter + 1
                if counter == 40:
                    break
                queue.append(url)
            await ctx.send(f"{counter} songs were added to queue", delete_after=5)
        else:
            url = search
            if not 'youtube' or not 'youtu.be' in url:
                await ctx.send('This is not a Youtube link, I cannot open this!')
            else:
                queue.append(url)
                await ctx.send(f'{url} was added to queue', delete_after=5)
        #player
        try:
            if not ctx.voice_client.is_playing():
                player_embed = discord.Embed()
                player_embed.title = f'{self.bot.user.name} Music Player... loading'
                player_embed.set_thumbnail(url=self.bot.user.avatar_url)
                player_embed.color = 0x206694
                player_embed.set_footer(text=f'{self.bot.user.name} is now linked to {ctx.voice_client.channel.name} 📌')
                player_msg = await ctx.send(embed = player_embed)
                while queue != []:
                    async with ctx.typing():
                        playurl = queue[0]
                        queue.remove(playurl)
                        player = await YTDLSource.from_url(playurl, loop=self.bot.loop, stream=True)
                        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    while ctx.voice_client.is_playing():
                        player_embed.title = ('Now playing: {}'.format(player.title))
                        player_embed.description = '\n'.join(queue)
                        await player_msg.edit(embed = player_embed)
                        await asyncio.sleep(5)
                await player_msg.delete()
                await ctx.send(embed = discord.Embed(title = f'{self.bot.user.name} music player'), description = (f'{ctx.message.author.mention} | There are no more songs in the queue to play 🎵')))
                await ctx.invoke(self.bot.get_command('stop'))
        except:
            await ctx.invoke(self.bot.get_command('stop'))
            return

    @commands.command(
        name="remove",
        help="Removes a song from the queue"
    )
    async def remove(self, ctx):
        try:
            await ctx.invoke(self.bot.get_command('queue'))
        except:
            return
        await ctx.send('Which song do you wish to remove? (copy the entire url and paste it)')
        msg = await self.bot.wait_for('message')
        if msg.content in queue:
            queue.remove(msg.content)
            await ctx.send(f'{msg.content} was removed from queue')
            return
            
            
        

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command(
        name="clearqueue",
        help="clears the queue"
    )
    async def clearqueue(self, ctx):
        queue = []

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.invoke(self.bot.get_command('clearqueue'))
        if not ctx.voice_client is None:
            await ctx.voice_client.disconnect()
        return

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")

def setup(bot):
    bot.add_cog(Music(bot))