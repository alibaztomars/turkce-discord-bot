import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import json
import os
import random

class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaways = []
        self.load_giveaways()
        self.check_giveaways.start()

    def load_giveaways(self):
        if os.path.exists('giveaways.json'):
            with open('giveaways.json', 'r') as file:
                self.giveaways = json.load(file)

    def save_giveaways(self):
        with open('giveaways.json', 'w') as file:
            json.dump(self.giveaways, file)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def çekiliş_oluştur(self, ctx, süre: str, *, ödül: str):
        süre_saniye = self.convert_to_seconds(süre)
        if süre_saniye is None:
            await ctx.send('Geçersiz süre formatı. Lütfen saat, dakika veya gün olarak belirtin.')
            return

        bitiş_zamanı = datetime.datetime.utcnow() + datetime.timedelta(seconds=süre_saniye)
        çekiliş = {
            "channel_id": ctx.channel.id,
            "message_id": None,
            "end_time": bitiş_zamanı.timestamp(),
            "prize": ödül,
            "participants": []
        }
        self.giveaways.append(çekiliş)
        self.save_giveaways()

        #kalan_süre_timestamp = f"<t:{int(bitiş_zamanı.timestamp())}:R>"
        bitiş_zamanı_str = bitiş_zamanı.strftime("%Y-%m-%d %H:%M:%S UTC")
        embed = discord.Embed(title="Çekiliş!", description=f"Ödül: {ödül}\nBitiş Zamanı: {bitiş_zamanı_str}", color=discord.Color.blue())
        view = discord.ui.View()
        join_button = discord.ui.Button(label="Katıl", style=discord.ButtonStyle.primary, custom_id="join_giveaway")
        view.add_item(join_button)
        message = await ctx.send(embed=embed, view=view)

        çekiliş["message_id"] = message.id
        self.save_giveaways()

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.data["custom_id"] == "join_giveaway":
            for çekiliş in self.giveaways:
                if çekiliş["message_id"] == interaction.message.id:
                    if interaction.user.id in çekiliş["participants"]:
                        await interaction.response.send_message("Zaten çekilişe katıldınız.", ephemeral=True)
                        leave_button = discord.ui.Button(label="Çekilişten Ayrıl", style=discord.ButtonStyle.danger, custom_id="leave_giveaway")
                        view = discord.ui.View()
                        view.add_item(leave_button)
                        await interaction.followup.send("Çekilişten ayrılmak için butona tıklayın.", view=view, ephemeral=True)
                    else:
                        çekiliş["participants"].append(interaction.user.id)
                        self.save_giveaways()
                        await interaction.response.send_message("Çekilişe katıldınız!", ephemeral=True)
        elif interaction.data["custom_id"] == "leave_giveaway":
            for çekiliş in self.giveaways:
                if interaction.user.id in çekiliş["participants"]:
                    çekiliş["participants"].remove(interaction.user.id)
                    self.save_giveaways()
                    await interaction.response.send_message("Çekilişten ayrıldınız.", ephemeral=True)
                    return
            await interaction.response.send_message("Çekilişe katılmamışsınız.", ephemeral=True)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def çekiliş_iptal(self, ctx, message_id: int):
        for çekiliş in self.giveaways:
            if çekiliş["message_id"] == message_id:
                channel = self.bot.get_channel(çekiliş["channel_id"])
                message = await channel.fetch_message(message_id)
                await message.delete()
                self.giveaways.remove(çekiliş)
                self.save_giveaways()
                await ctx.send('Çekiliş iptal edildi ve mesaj silindi.')
                return
        await ctx.send('Çekiliş bulunamadı.')

    @tasks.loop(seconds=60)
    async def check_giveaways(self):
        current_time = datetime.datetime.utcnow().timestamp()
        for çekiliş in self.giveaways[:]:
            if current_time >= çekiliş["end_time"]:
                channel = self.bot.get_channel(çekiliş["channel_id"])
                message = await channel.fetch_message(çekiliş["message_id"])
                if çekiliş["participants"]:
                    winner_id = random.choice(çekiliş["participants"])
                    winner = self.bot.get_user(winner_id)
                    await channel.send(f'Tebrikler {winner.mention}! {çekiliş["prize"]} kazandınız!')
                    embed = message.embeds[0]
                    embed.description += "\nÇekiliş bitti."
                    await message.edit(embed=embed)
                else:
                    await channel.send('Çekilişe kimse katılmadı.')
                    embed = message.embeds[0]
                    embed.description += "\nÇekiliş bitti. Katılım olmadı."
                    await message.edit(embed=embed)
                self.giveaways.remove(çekiliş)
                self.save_giveaways()

    def convert_to_seconds(self, süre: str):
        try:
            if süre.endswith('s'):
                return int(süre[:-1])
            elif süre.endswith('m'):
                return int(süre[:-1]) * 60
            elif süre.endswith('h'):
                return int(süre[:-1]) * 3600
            elif süre.endswith('d'):
                return int(süre[:-1]) * 86400
        except ValueError:
            return None

async def setup(bot):
    await bot.add_cog(Giveaways(bot))
