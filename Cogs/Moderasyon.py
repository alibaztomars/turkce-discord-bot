import discord
from discord.ext import commands
#import datetime #timeout komutu hata veriyor. Ve bu yüzden bunu kullanamıyoruz. Kullanılacaksa datetime import etmemiz gerekiyor.

class Moderasyon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def temizle(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send(f'{limit} mesaj silindi.', delete_after=5)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def banla(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} banlandı. Sebep: {reason}')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def at(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} atıldı. Sebep: {reason}')

    #timeout komutu hata veriyor. Ve bu yüzden bunu kullanamıyoruz. Kullanılacaksa datetime import etmemiz gerekiyor.
    """
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason=None):
        current_time = datetime.datetime.utcnow()
        duration = current_time + datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f'{member.mention} {minutes} dakika boyunca timeoutlandı. Sebep: {reason}')
    """
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def rol_ekle(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f'{member.mention} kullanıcısına {role.name} rolü eklendi.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def rol_sil(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} kullanıcısından {role.name} rolü kaldırıldı.')


async def setup(bot):
    await bot.add_cog(Moderasyon(bot))
