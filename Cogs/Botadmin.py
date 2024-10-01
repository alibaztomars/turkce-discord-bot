import discord
from discord.ext import commands
from Database.Database import Database
from config import botadmins
import ast

class Botadmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    def cog_check(self, ctx):
        return ctx.author.id in botadmins

    @commands.command()
    async def set_bakiye(self, ctx, member: discord.Member, amount: int):
        if ctx.author.id not in botadmins:
            await ctx.send('Bu komutu kullanma yetkiniz yok.')
            return
        user_data = self.db.get_user_data(member.id)
        if user_data is None:
            self.db.create_new_user(member.id)
            user_data = {"level": 1, "xp": 0, "balance": amount}
        else:
            user_data["balance"] = amount
        self.db.save_user_data(member.id, user_data)
        await ctx.send(f'{member.mention} kullanıcısının bakiyesi {amount} olarak ayarlandı.')

    @commands.command()
    async def set_seviye(self, ctx, member: discord.Member, level: int, xp: int = 0):
        if ctx.author.id not in botadmins:
            await ctx.send('Bu komutu kullanma yetkiniz yok.')
            return
        user_data = self.db.get_user_data(member.id)
        if user_data is None:
            self.db.create_new_user(member.id)
            user_data = {"level": level, "xp": xp}
            
        else:
            user_data["level"] = level
            user_data["xp"] = xp
        self.db.save_user_data(member.id, user_data)
        await ctx.send(f'{member.mention} kullanıcısının seviyesi {level} ve XP\'si {xp} olarak ayarlandı.')

    @commands.command()
    async def get_user_data(self, ctx, member: discord.Member):
        if ctx.author.id not in botadmins:
            await ctx.send('Bu komutu kullanma yetkiniz yok.')
            return
        user_data = self.db.get_user_data(member.id)
        if user_data is None:
            await ctx.send(f'{member.mention} kullanıcısının verisi bulunamadı.')
        else:
            await ctx.send(f'{member.mention} kullanıcısının verisi: {user_data}')

    @commands.command()
    async def set_user_data(self, ctx, member: discord.Member, *, data: str):
        if ctx.author.id not in botadmins:
            await ctx.send('Bu komutu kullanma yetkiniz yok.')
            return
        
        try:
            user_data = ast.literal_eval(data)
            if not isinstance(user_data, dict):
                raise ValueError
        except (SyntaxError, ValueError) as e:
            await ctx.send(f'Geçersiz Python dict formatı. Hata: {e}')
            return
        
        self.db.save_user_data(member.id, user_data)
        await ctx.send(f'{member.mention} kullanıcısının verisi güncellendi: {user_data}')


    @commands.command()
    async def change_status(self, ctx, *, status: str):
        if ctx.author.id not in botadmins:
            await ctx.send('Bu komutu kullanma yetkiniz yok.')
            return
        await self.bot.change_presence(activity=discord.Game(name=status))
        await ctx.send(f'Botun durumu "{status}" olarak değiştirildi.')

    @commands.command()
    async def send_error_logs(self, ctx):
        if ctx.author.id not in botadmins:
            await ctx.send('Bu komutu kullanma yetkiniz yok.')
            return
        with open('error_logs.txt', 'r') as file:
            logs = file.read()
        if len(logs) > 2000:
            await ctx.send(file=discord.File('error_logs.txt'))
        else:
            await ctx.send(f'```{logs}```')

async def setup(bot):
    await bot.add_cog(Botadmin(bot))

