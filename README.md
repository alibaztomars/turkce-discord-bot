# turkce-discord-bot
Kendi sunucunuz için kendi özel Discord botunuz.

# Discord Bot

Bu proje, Discord sunucunuzda çeşitli komutlar ve etkileşimler sağlayan bir Discord botudur. Bot, moderasyon, seviye, ekonomi, bot yönetimi ve çekilişler gibi çeşitli kategorilerde komutlar sunar.

## Özellikler

- **Moderasyon Komutları**: Mesaj temizleme, kullanıcı banlama, kullanıcı atma, rol ekleme ve rol silme.
- **Seviye Komutları**: Kullanıcı seviyesini gösterme. Seviye atlama.
- **Ekonomi Komutları**: Kullanıcı bakiyesini gösterme, para kazanma, coin flip, liderlik tablosu.
- **Botadmin Komutları**: Kullanıcı bakiyesini ve seviyesini ayarlama, kullanıcı verilerini gösterme ve ayarlama, bot durumunu değiştirme, hata loglarını gönderme.
- **Çekiliş Komutları**: Çekiliş oluşturma ve iptal etme.

## Kurulum

### Gereksinimler

- Python 3.8 veya daha üstü
- `discord.py` kütüphanesi
- `discord.ext` kütüphanesi

### Adımlar

1. **Depoyu Klonlayın**

    ```bash
    git clone https://github.com/kullaniciadi/discord-bot.git
    cd discord-bot
    ```

2. **Gerekli Kütüphaneleri Yükleyin**

    ```bash
    pip install -r requirements.txt
    ```

3. **Bot Token'ınızı Ayarlayın**

    `config.py` dosyasını oluşturun ve Discord bot token'ınızı ekleyin:

    ```python
    token = 'YOUR_DISCORD_BOT_TOKEN'
    ```

4. **Botu Çalıştırın**

    ```bash
    python main.py
    ```

## Kullanım

Bot çalıştığında, Discord sunucunuzda çeşitli komutları kullanabilirsiniz. Yardım komutunu kullanarak mevcut komutları ve kategorileri görebilirsiniz.

## Hata Ayıklama

Bot çalışırken herhangi bir hata ile karşılaşırsanız, `error_logs.txt` dosyasını kontrol edebilirsiniz. Bu dosya, botun çalışması sırasında meydana gelen hataları kaydeder.

## Önemli bir not

Bot tek sunucu için tasarlanmış ve yazılmıştır. Botunuzun başka sunuculara girmesini önlemek için Discord Developer Portal'dan botunuzun Public Bot ayarının kapalı olduğundan emin olun.
