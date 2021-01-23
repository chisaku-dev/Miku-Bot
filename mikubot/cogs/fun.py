from discord.ext import commands
import discord
import random

class Fun(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        name='roshambo',
        help='play roshambo with Miku [rock/paper/scissor]',
        pass_context=True
    )
    async def roshambo(self, ctx):
        #get user input
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        await ctx.send('Type rock, paper or scissor!')
        msg = await self.bot.wait_for('message', check=check)
        person1 = msg.content
        person1 = person1.lower()
        #miku decision
        mikuhand = random.randint(0,2)
        handformations=['rock', 'scissor', 'paper']
        #gamelogic
        if person1 != 'rock' and person1 != 'scissor' and person1 != 'paper':
            await ctx.send("Don't cheat, I'm watching you! 👀")
        else:
            if person1 == 'rock':
                if handformations[mikuhand] == 'rock':
                    winmatch = 'tie'
                elif handformations[mikuhand] == 'scissor':
                    winmatch = 'win 👑'
                elif handformations[mikuhand] == 'paper':
                    winmatch = 'lose'
            elif person1 == 'scissor':
                if handformations[mikuhand] == 'rock':
                    winmatch = 'lose'
                elif handformations[mikuhand] == 'scissor':
                    winmatch = 'tie'
                elif handformations[mikuhand] == 'paper':
                    winmatch = 'win 👑'
            elif person1 == 'paper':
                if handformations[mikuhand] == 'rock':
                    winmatch = 'win 👑'
                elif handformations[mikuhand] == 'scissor':
                    winmatch = 'lose'
                elif handformations[mikuhand] == 'paper':
                    winmatch = 'tie'
            await ctx.send(f'Miku used **{handformations[mikuhand]}** vs your **{person1}**. You **{winmatch}**!')
            return
        
    @commands.command(
        name='ship',
        help='Miku measures the love compatibility between two individuals',
        pass_context=True
    )
    async def ship(self, ctx, person1, person2):
        if person1 == person2:
            await ctx.send("I can't ship a person with themselves! 👉👈")
        else:
            compatibility = random.randint(0, 100)
            await ctx.send(f'Miku thinks {person1} and {person2} have a {compatibility} percent compatibility ❤!')
        return
    
    @commands.command(
        name="kill",
        help="Hitgirl gonna kill some folks",
        pass_context=True
    )
    async def kill(self, ctx, person):
        phrasechoice = random.randint(0, 2)
        phrase = ["Headshots", "Slits the throat of", "Drowns"]
        matchinggif = ['https://media1.tenor.com/images/125b5a839eb39979c8cc02d1a77bd8b4/tenor.gif?itemid=11956086' , 'https://i.pinimg.com/originals/d3/d6/32/d3d632461ad43f6af520f6ffdc290f81.gif', 'https://68.media.tumblr.com/tumblr_lvmlnxRqXF1qbghoko1_500.gif']
        await ctx.send('{} {} {} !'.format(phrase[phrasechoice], person, matchinggif[phrasechoice]))
        return

    @commands.command(
        name='coinflip',
        help='Miku flips a coin to help solve disputes!',
        pass_context=True
    )
    async def coinflip(self, ctx):
        coinflip=random.randint(1, 2)
        if coinflip == 1:
            await ctx.send('Heads')
        else:
            await ctx.send('Tails')
        return

    @commands.command(
        name="simp",
        help="rates your simpness",
        pass_context=True
    )
    async def simprating(self, ctx, person1):
        rating = random.randint(0, 100)
        await ctx.send('{} is {}% simp!'.format(person1, rating))
        return

    @commands.command(
        name="numbergame",
        help="Play a guessing number game!",
        pass_context=True
    )
    async def randomgame(self, ctx):
        randomnumber = random.randint(0, 10)
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        await ctx.send('State a number between 0 and 10!')
        msg = await self.bot.wait_for('message', check=check)
        numberinput = int(float(msg.content))
        if randomnumber == numberinput:
            await ctx.send(f"You are correct! Both you and Miku chose {randomnumber}!")
        else:
            await ctx.send(f"You guessed wrongly, Miku chose {randomnumber} and you chose {numberinput}! Better luck next time!")
        return


def setup(bot):
    bot.add_cog(Fun(bot))