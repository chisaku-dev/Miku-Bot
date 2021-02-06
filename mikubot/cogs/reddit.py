from discord.ext import commands
import discord

import random
import praw
import sqlite3

def redditkey():
    con = sqlite3.connect('./bot.db')
    con.execute('CREATE TABLE IF NOT EXISTS reddit (id VARCHAR(255), secret TEXT);')
    con.commit()
    choices = ['add new reddit API key', 'use existing reddit API key']
    while True:
        for i in range(0, len(choices)):
            print(i, choices[i])
        choice = int(input('Enter what you want to: '))
        if choice == 0:
            con.execute('INSERT INTO reddit (id, secret) VALUES (?, ?)', (input('redditid: '), input('redditsecret: ')))
            con.commit()
            print('Successfully added reddit API key')
        elif choice == 1:
            cursor = con.cursor()
            cursor.execute('SELECT id FROM reddit')
            keys = cursor.fetchall()
            for i in range(0, len(keys)):
                print(i, keys[0][i])
            key_to_use = int(input('Enter the number of the reddit api key you wish to use: '))
            cursor.execute('SELECT secret FROM reddit WHERE id = ?', [keys[0][key_to_use],])
            secret = cursor.fetchone()
            print('Successfully connected!\nThe bot is now active')
            return (keys[0][key_to_use], secret[0])

cred = redditkey()
redditapi = praw.Reddit(
    client_id=cred[0],
    client_secret=cred[1],
    user_agent="Discord"
)

class reddit(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name="art",
        help="Miku finds a fanart of herself!"
    )
    async def art(self, ctx):
        searchtopics = ['hatsune miku art', 'hatsune art', 'miku hatsune art', 'r/hatsune']

        searchterm = searchtopics[random.randint(0, len(searchtopics)-1)]
        await ctx.invoke(self.bot.get_command('reddit'), search = searchterm)

    @commands.command(
        name="waifuart",
        help="Miku finds fanarts of waifus!"
    )
    async def waifuart(self, ctx):
        searchtopics = ['waifu art', 'anime girl art', 'pixiv girl', 'project sekai', 'zero two',
        'mikasa ackerman', 'kyoani girl', 'genshin girl', 'hololive fanart', 'tohsaka', 'tsukasa yuzaki', 'fubuki',
        'okayu', 'gawr gura', 'rin kagamine', 'ddlc', 'meiko vocaloid', 'chizuru mizuhara', 'r/CuteAnimeArts', 'r/MoeStash',
        'r/AnimeWallpapersSFW']
        
        searchterm = searchtopics[random.randint(0, len(searchtopics)-1)]
        await ctx.invoke(self.bot.get_command('reddit'), search = searchterm)
    
    
    @commands.command(
        name="husbandoart",
        help="Miku finds fanarts of husbandos!"
    )
    async def husbandoart(self, ctx):
        searchtopics = ['anime boy', 'ganyu', 'husbando art', 'levi ackerman', 'sebastian michaelis', 'rin okumura',
        'makoto tachibana', 'takumi usui', 'sasuke', 'sasuke uchiha', 'todaroki shouto', 'todaroki', 'zero kiryu',
        'victor nikiforov', 'vildred']
        searchterm = searchtopics[random.randint(0, len(searchtopics)-1)]
        await ctx.invoke(self.bot.get_command('reddit'), search = searchterm)

    @commands.command(
        name="meme",
        help="Miku finds a meme"
    )
    async def meme(self, ctx):
        searchtopics = [' ', 'dank', 'anime', 'christian', 'tech ', 'funny ', 'coding ', 'reddit ', 'music ',
        'manga ', 'school ', 'relatable ']

        searchterm = searchtopics[random.randint(0, len(searchtopics)-1)] + 'memes'
        await ctx.invoke(self.bot.get_command('reddit'), search = searchterm)

    @commands.command(
        name="reddit",
        help="Miku browses on reddit"
    )
    async def reddit(self, ctx, *, search: str):
        print(search, '|', end=' ')
        if 'r/' in search:
            #treat as subreddit
            search = search.split('/')
            sub = search[1]
            search = 'all'
        else:
            #treat as general search
            sub = 'all'
        randomsort = ['top', 'hot', 'relevance']
        sortmethod = random.randint(0, len(randomsort)-1)
        limitsearch = 25
        while True:
            prawquery = redditapi.subreddit(sub).search(search, sort=randomsort[sortmethod], limit=limitsearch)
            posts = [post for post in prawquery if '.jpg' in post.url or '.png' in post.url or '.gif' in post.url and not post.over_18 and not post.subreddit.over18]
            if len(posts) > 10:
                print(len(posts), 'posts found |', limitsearch, ' posts scope |', 'sorted with', randomsort[sortmethod], '|', (len(posts)*100)/limitsearch, '% suitable')
                break
            else:
                if sortmethod == len(randomsort) - 1:
                    sortmethod = 0
                else:
                    sortmethod += 1
                limitsearch += 25
                if limitsearch == 75:
                    print('FAIL', len(posts), 'posts found |', limitsearch, ' posts scope |', 'sorted with', randomsort[sortmethod], '|', (len(posts)*100)/limitsearch, '% suitable')
                    await ctx.send('Not enough suitable posts were found')
                    return
        submission = posts[random.randint(0, len(posts)-1)]
        reddit_embed = discord.Embed()
        reddit_embed.description = f'Miku found this post in r/{submission.subreddit.display_name} by {submission.author.name}'
        reddit_embed.set_image(url=submission.url)
        await ctx.send(embed=reddit_embed)

def setup(bot):
    bot.add_cog(reddit(bot))