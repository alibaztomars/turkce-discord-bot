import discord
from discord.ext import commands
import json
from Database.Database import Database  # veya uygun modülden içe aktarın

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()  # veya uygun şekilde başlatın

    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            user_id = ctx.author.id
            user_data = self.db.get_user_data(user_id)  # self.db kullanın
            if user_data is None:
                await ctx.send(f'{ctx.author.mention}, you do not have an account yet.')
            else:
                balance = user_data.get('balance', 0)
                await ctx.send(f'{ctx.author.mention}, your balance is {balance} coins.')
        else:
            user_id = member.id
            user_data = self.db.get_user_data(user_id)  # self.db kullanın
            if user_data is None:
                await ctx.send(f'{member.mention} does not have an account yet.')
            else:
                balance = user_data.get('balance', 0)
                await ctx.send(f'{member.mention}, their balance is {balance} coins.')

    @commands.command()
    async def earn(self, ctx):
        user_id = ctx.author.id
        user_data = self.db.get_user_data(user_id)  # self.db kullanın
        if user_data is None:
            self.db.create_new_user(user_id)
            user_data = self.db.get_user_data(user_id)
        
        balance = user_data.get('balance', 0)
        balance += 10
        user_data['balance'] = balance
        self.db.save_user_data(user_id, user_data)
        await ctx.send(f'{ctx.author.mention}, you earned 10 coins. Your new balance is {balance} coins.')

    @commands.command()
    async def leaderboard(self, ctx):
        self.db.cursor.execute('SELECT id, data FROM users')
        users = self.db.cursor.fetchall()
        
        if not users:
            await ctx.send('No users found in the database.')
            return
        
        leaderboard = []
        for user in users:
            user_id, data = user
            user_data = json.loads(data)
            balance = user_data.get('balance', 0)
            leaderboard.append((user_id, balance))
        
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        top_10 = leaderboard[:10]
        
        if not top_10:
            await ctx.send('No users have a balance yet.')
            return
        
        embed = discord.Embed(title="Leaderboard", description="Top 10 users with the highest balance", color=discord.Color.gold())
        for i, (user_id, balance) in enumerate(top_10, start=1):
            user = self.bot.get_user(user_id)
            if user:
                embed.add_field(name=f"{i}. {user.name}", value=f"{balance} coins", inline=False)
            else:
                embed.add_field(name=f"{i}. Unknown User (ID: {user_id})", value=f"{balance} coins", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def coinflip(self, ctx, bet):
        user_id = ctx.author.id
        user_data = self.db.get_user_data(user_id)
        
        if user_data is None:
            await ctx.send(f'{ctx.author.mention}, you do not have an account. Use the earn command to create one.')
            return
        
        balance = user_data.get('balance', 0)
        
        if bet == "all":
            bet = min(max(balance, 20), 100)
        else:
            try:
                bet = int(bet)
            except ValueError:
                await ctx.send(f'{ctx.author.mention}, your bet must be a number or "all".')
                return
        
        if bet < 20 or bet > 100:
            await ctx.send(f'{ctx.author.mention}, your bet must be between 20 and 100 coins.')
            return
        
        if bet > balance:
            await ctx.send(f'{ctx.author.mention}, you do not have enough balance to place this bet.')
            return
        
        import random
        result = random.choice(['heads', 'tails'])
        user_choice = random.choice(['heads', 'tails'])
        
        if user_choice == result:
            balance += bet
            await ctx.send(f'{ctx.author.mention}, you won the coin flip! Your new balance is {balance} coins.')
        else:
            balance -= bet
            await ctx.send(f'{ctx.author.mention}, you lost the coin flip. Your new balance is {balance} coins.')
        
        user_data['balance'] = balance
        self.db.save_user_data(user_id, user_data)



async def setup(bot):
    await bot.add_cog(Economy(bot))
