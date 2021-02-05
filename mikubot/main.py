import discord
from discord.ext import commands
import random
import asyncio
import sqlite3
#saving bot tokens in database
def key():
    try:
        con = sqlite3.connect('./bot.db')
        con.execute('CREATE TABLE IF NOT EXISTS botkeys (botname VARCHAR(255) NOT NULL UNIQUE, key VARCHAR(255) NOT NULL UNIQUE);')
        con.commit()
        print('table initialized')
    except sqlite3.Error as e:
        print('Error', e)
    choices = ['add new bot', 'run existing bot', 'update key']
    con = sqlite3.connect('./bot.db')
    while True:
        for i in range(0, len(choices)):
            print(i, choices[i])
        chosentask = int(input("Enter what you want to do: "))
        if chosentask == 0:
            #add new bot
            try:
                name = input('What is the name of the bot?\n')
                while True:
                    key = input('What is the bot key? (This will be stored in the local database called "bot.db")\n')
                    if len(key) > 20:
                        break
                    else:
                        print('This is not a key')
                insert_sql = 'INSERT INTO botkeys (botname, key) VALUES (?, ?)'
                con.execute(insert_sql, (name, key))
                con.commit()
                print(f'Successfully created bot {name}')
            except sqlite3.Error as e:
                print('Error:', e)
        elif chosentask == 1:
            #run existing bot
            try:
                cursor = con.cursor()
                cursor.execute('SELECT botname FROM botkeys;')
                botnames = cursor.fetchall()
                for i in range(0, len(botnames)):
                    print(botnames[0][i])
                name = input('Enter the name of the bot: ')
                selectkey = 'SELECT key FROM botkeys WHERE botname = ?;'
                cursor.execute(selectkey, [name,])
                key = cursor.fetchone()
                return key[0]
            except sqlite3.Error as e:
                print('Error:', e)
        elif chosentask == 2:
            try:
                cursor = con.cursor()
                cursor.execute('SELECT botname FROM botkeys;')
                botnames = cursor.fetchall()
                for i in range(0, len(botnames)):
                    print(botnames[0][i])
                name = input('Enter the name of the bot: ')
                while True:
                    newkey = input('What is the new key?\n')
                    if len(newkey) > 20:
                        break
                    else:
                        print('This is not a key')
                con.execute('UPDATE botkeys SET key = ? WHERE botname = ?', [name, newkey])
                con.commit()
                print('Key updated')
            except sqlite3.Error as e:
                print('Error:', e)
        else:
            print('That is not a valid task')

#start bot
def get_prefix(client, message):

    prefixes = ['Miku ', 'miku ']

    return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(
    command_prefix=get_prefix,
    help='A Miku bot',
    case_insensitive=True
)

TOKEN = key()

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
    print(f'Logged in as {bot.user.name} - {bot.user.id} Awaiting Reddit API...')
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
                    #if the channel is named global
                    message_embed = discord.Embed()
                    message_embed.set_footer(
                        text=f'Sent by {message.author.name} at {message.author.guild.name}',
                        icon_url=message.author.avatar_url
                    )
                    if 'http' in message.content:
                        seperated = message.content.split(' ')
                        strip = 0
                        while strip != len(seperated):
                            if 'http' in seperated[strip]:
                                #locate the strip of text containing the link
                                break
                            else:
                                strip = strip + 1
                        if 'tenor' in seperated[strip]:
                            await channel.send(seperated[strip])
                        else:
                            message_embed.set_image(url = str(seperated[strip]))
                    #if there are attachments
                    try:
                        message_embed.set_image(url = message.attachments[0].url)
                    except:
                        await asyncio.sleep(0)
                    #send the embed message
                    message_embed.description = message.content
                    await channel.send(embed=message_embed)
    else:
        await bot.process_commands(message)

bot.run(TOKEN, bot=True, reconnect=True)