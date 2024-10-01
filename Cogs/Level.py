import discord
from discord.ext import commands
from Database.Database import Database

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        user_data = self.db.get_user_data(user_id)

        if user_data is None:
            self.db.create_new_user(user_id)
            user_data = {"level": 1, "xp": 0}

        user_data["xp"] += 10  # Her mesaj için 10 XP ekle
        next_level_xp = user_data["level"] * 100  # Bir sonraki seviye için gereken XP

        if user_data["xp"] >= next_level_xp:  # Gereken XP'ye ulaşıldığında seviye atla
            user_data["level"] += 1
            user_data["xp"] = 0
            await message.channel.send(f'Tebrikler {message.author.mention}, seviye atladınız! Şu anki seviyeniz: {user_data["level"]}')

        self.db.save_user_data(user_id, user_data)

    @commands.command()
    async def seviye(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        user_id = member.id
        user_data = self.db.get_user_data(user_id)

        if user_data is None:
            if member == ctx.author:
                await ctx.send('Henüz bir seviyeniz yok. Mesaj yazarak seviye kazanmaya başlayabilirsiniz.')
            else:
                await ctx.send(f'{member.display_name} henüz bir seviyeye sahip değil.')
        else:
            next_level_xp = user_data["level"] * 100  # Bir sonraki seviye için gereken XP
            if member == ctx.author:
                await ctx.send(f'{member.mention}, şu anki seviyeniz: {user_data["level"]}, XP: {user_data["xp"]}/{next_level_xp}')
            else:
                await ctx.send(f'{member.mention}\'in seviyesi: {user_data["level"]}, XP: {user_data["xp"]}/{next_level_xp}')

async def setup(bot):
    await bot.add_cog(Level(bot))
