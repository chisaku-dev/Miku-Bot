from discord.ext import commands
import discord

import random
import praw

redditapi = praw.Reddit(
    client_id=input('Reddit client_id: '),
    client_secret=input('Reddit client_secret: '),
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
        searchtopics = ['loli art', 'waifu art', 'anime girl art', 'pixiv girl art', 'pixiv art', 'project sekai', 'appreciart', 'zero two art', 'mikasa ackerman art', 'kyoani girl', 'genshin art']
        
        searchterm = searchtopics[random.randint(0, len(searchtopics)-1)]
        await ctx.invoke(self.bot.get_command('reddit'), search = searchterm)
    
    
    @commands.command(
        name="husbandoart",
        help="Miku finds fanarts of husbandos!"
    )
    async def husbandoart(self, ctx):
        await ctx.invoke(self.bot.get_command('reddit'), search = 'husbando art')

    @commands.command(
        name="meme",
        help="Miku finds a meme"
    )
    async def meme(self, ctx):
        searchtopics = ['memes', 'dankmemes', 'animememes', 'christianmemes', 'tech memes', 'funny memes']

        searchterm = searchtopics[random.randint(0, len(searchtopics)-1)]
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
        limitsearch = 50
        while True:
            prawquery = redditapi.subreddit(sub).search(search, sort=randomsort[sortmethod], limit=limitsearch)
            posts = [post for post in prawquery if 'jpg' in post.url or 'gif' in post.url and not post.over_18 and not post.link_flair_text == None]
            if len(posts) > 10:
                print(len(posts), 'posts found |', limitsearch, ' posts scope |', 'sorted with', randomsort[sortmethod], '|', (len(posts)*100)/limitsearch, '% suitable')
                break
            else:
                if sortmethod == len(randomsort) - 1:
                    sortmethod = 0
                else:
                    sortmethod += 1
                limitsearch += 25
                if limitsearch == 200:
                    print('FAIL', len(posts), 'posts found |', limitsearch, ' posts scope |', 'sorted with', randomsort[sortmethod], '|', (len(posts)*100)/limitsearch, '% suitable')
                    await ctx.send('Not enough suitable posts were found')
                    return
        submission = posts[random.randint(0, len(posts)-1)]
        await ctx.send(submission.url)

def setup(bot):
    bot.add_cog(reddit(bot))