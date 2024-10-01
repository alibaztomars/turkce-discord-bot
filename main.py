import discord
from discord.ext import commands
from discord.ui import View, Button
import os
from config import token
import logging

# Loglama yapılandırması
logging.basicConfig(
    filename='error_logs.txt',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

class HelpView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Moderasyon", style=discord.ButtonStyle.primary, custom_id="moderasyon"))
        self.add_item(Button(label="Seviye", style=discord.ButtonStyle.primary, custom_id="seviye"))
        self.add_item(Button(label="Ekonomi", style=discord.ButtonStyle.primary, custom_id="ekonomi"))
        self.add_item(Button(label="Botadmin", style=discord.ButtonStyle.primary, custom_id="botadmin"))
        self.add_item(Button(label="Çekilişler", style=discord.ButtonStyle.primary, custom_id="çekilişler"))

async def load_extensions():
    for filename in os.listdir('./Cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'Cogs.{filename[:-3]}')
            except Exception as e:
                print(f'Failed to load extension {filename}: {e}')
                logging.error(f'Failed to load extension {filename}: {e}', exc_info=True)

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!help"))
    await load_extensions()
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{error.param.name} argümanını eksik girdiniz.')
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'{error.param.name} argümanı sayı olmalıdır.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Yetersiz yetki.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Böyle bir komut yok. komut listesi için !help yazabilirsiniz.')
    else:
        await ctx.send('Beklenmeyen bir hata ile karşılaşıldı.')
        logging.error(f'Error: {error}', exc_info=True)

@bot.command()
async def help(ctx):
    view = HelpView()
    await ctx.send("Yardım kategorisini seçin:", view=view)

@bot.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "moderasyon":
            embed = discord.Embed(title="Moderasyon Komutları", description="---", color=0x00ff00)
            embed.add_field(name="!temizle <limit>", value="Belirtilen sayıda mesajı siler. (Yönetici yetkisi gerektirir)", inline=False)
            embed.add_field(name="!banla <kullanıcı> [sebep]", value="Belirtilen kullanıcıyı banlar. (Ban yetkisi gerektirir)", inline=False)
            embed.add_field(name="!at <kullanıcı> [sebep]", value="Belirtilen kullanıcıyı sunucudan atar. (Atma yetkisi gerektirir)", inline=False)
            embed.add_field(name="!rol_ekle <kullanıcı> <rol>", value="Belirtilen kullanıcıya rol ekler. (Rol yönetme yetkisi gerektirir)", inline=False)
            embed.add_field(name="!rol_sil <kullanıcı> <rol>", value="Belirtilen kullanıcıdan rolü kaldırır. (Rol yönetme yetkisi gerektirir)", inline=False)
        elif interaction.data["custom_id"] == "seviye":
            embed = discord.Embed(title="Seviye Komutları", description="---", color=0x00ff00)
            embed.add_field(name="!seviye [kullanıcı]", value="Kullanıcının seviyesini gösterir. Kullanıcı belirtilmezse komutu kullanan kişinin seviyesini gösterir.", inline=False)
        elif interaction.data["custom_id"] == "ekonomi":
            embed = discord.Embed(title="Ekonomi Komutları", description="---", color=0x00ff00)
            embed.add_field(name="!bakiye [kullanıcı]", value="Kullanıcının bakiyesini gösterir. Kullanıcı belirtilmezse komutu kullanan kişinin bakiyesini gösterir.", inline=False)
            embed.add_field(name="!earn", value="10 para kazanırsın.", inline=False)
            embed.add_field(name="!coinflip <miktar>", value="Belirtilen miktarda coin flip atar. all yazarsan tüm para ile oynarsın. (20-100 arası oynanabilir)", inline=False)
            embed.add_field(name="!leaderboard", value="En çok coin sahibi 10 kişiyi gösterir.", inline=False)
        elif interaction.data["custom_id"] == "botadmin":
            embed = discord.Embed(title="Botadmin Komutları", description="---", color=0x00ff00)
            embed.add_field(name="!set_bakiye <kullanıcı> <miktar>", value="Belirtilen kullanıcının bakiyesini ayarlar. (Botadmin yetkisi gerektirir)", inline=False)
            embed.add_field(name="!set_seviye <kullanıcı> <seviye> [xp]", value="Belirtilen kullanıcının seviyesini ve XP'sini ayarlar. (Botadmin yetkisi gerektirir)", inline=False)
            embed.add_field(name="!get_user_data <kullanıcı>", value="Belirtilen kullanıcının verilerini gösterir. (Botadmin yetkisi gerektirir)", inline=False)
            embed.add_field(name="!set_user_data <kullanıcı> <veri>", value="Belirtilen kullanıcının verilerini ayarlar. (Botadmin yetkisi gerektirir)", inline=False)
            embed.add_field(name="!change_status <durum>", value="Botun durumunu değiştirir. (Botadmin yetkisi gerektirir)", inline=False)
            embed.add_field(name="!send_error_logs", value="Hata loglarını gönderir. (Botadmin yetkisi gerektirir)", inline=False)
        elif interaction.data["custom_id"] == "çekilişler":
            embed = discord.Embed(title="Çekiliş Komutları", description="---", color=0x00ff00)
            embed.add_field(name="!çekiliş_oluştur <süre> <ödül>", value="Belirtilen süre ve ödülle bir çekiliş oluşturur. (Sunucu yönetme yetkisi gerektirir)", inline=False)
            embed.add_field(name="!çekiliş_iptal <mesaj_id>", value="Belirtilen mesaj ID'sine sahip çekilişi iptal eder. (Sunucu yönetme yetkisi gerektirir)", inline=False)
        
        #Aslında burada çekilişler cogsunun butonları yüzünden hata alıyor ve logging tarafından yakalanıyor. Ancak ekran çıktısına da yazdırıyor. Ekran çıktısına yazdırmayı önlemek için try except kullanıldı.
        try:
            await interaction.response.edit_message(embed=embed, view=HelpView())
        except Exception as e:
            logging.error(f'Error: {e}', exc_info=True)

bot.run(token)
