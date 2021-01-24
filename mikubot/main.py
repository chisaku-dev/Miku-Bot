import discord
from discord.ext import commands
import random
import asyncio

def get_prefix(client, message):

    prefixes = ['Miku ', 'miku ']

    return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(
    command_prefix=get_prefix,
    help='A Miku bot',
    case_insensitive=True
)

TOKEN = input('Bot Token: ')

cogs = ['cogs.description', 'cogs.basic', 'cogs.utility', 'cogs.fun', 'cogs.reddit', 'cogs.music', 'cogs.chess']

#custom help
class helpcommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=0x1ABC9C, description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

bot.help_command = helpcommand()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    for cog in cogs:
        bot.load_extension(cog)
    while True:
        await bot.change_presence(activity=discord.Activity(
            type = discord.ActivityType.playing,
            name=(f"Project Sekai and connecting {len(bot.guilds)} servers with the power of Music 🎵! Use [miku help] for more information!")))
        await asyncio.sleep(60)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

@bot.event
async def on_message(message):
    if not message.author.bot and message.channel.name == 'global':
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.name == 'global' and channel.id != message.channel.id:
                    message_embed = discord.Embed()
                    message_embed.set_footer(
                        text=f'Sent by {message.author.name} at {message.author.guild.name}',
                        icon_url=message.author.avatar_url
                    )
                    if '.gif' in message.content or '.png' in message.content or '.jpg' in message.content:
                        seperated = message.content.split(' ')
                        strip = 0
                        while strip != len(seperated):
                            if '.gif' in seperated[strip] or '.png' in seperated[strip] or '.jpg' in seperated[strip]:
                                break
                            else:
                                strip = strip + 1
                        message_embed.set_image(url = str(seperated[strip]))
                    try:
                        message_embed.set_image(url = message.attachments[0].url)
                    except:
                        await asyncio.sleep(0.5)
                    message_embed.description = message.content
                    await channel.send(embed=message_embed)
    else:
        await bot.process_commands(message)

bot.run(TOKEN, bot=True, reconnect=True)