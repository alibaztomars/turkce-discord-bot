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

### Adımlar

1. **Depoyu Klonlayın**

    ```bash
    git clone https://github.com/alibaztomars/turkce-discord-bot.git
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


### Komutlar ve Örnekler

#### Moderasyon Komutları

- **Mesaj Temizleme**: Belirli sayıda mesajı siler.
    ```bash
    !temizle 10
    ```

- **Kullanıcı Banlama**: Belirtilen kullanıcıyı banlar.
    ```bash
    !banla @kullanici Sebep burası
    ```

- **Kullanıcı Atma**: Belirtilen kullanıcıyı sunucudan atar.
    ```bash
    !at @kullanici Kurallar_yanlış
    ```

- **Rol Ekleme**: Belirtilen kullanıcıya rol ekler.
    ```bash
    !rol_ekle @kullanici RolAdi
    ```

- **Rol Silme**: Belirtilen kullanıcıdan rolü kaldırır.
    ```bash
    !rol_sil @kullanici RolAdi
    ```

#### Seviye Komutları

- **Seviye Gösterme**: Kullanıcının seviyesini gösterir.
    ```bash
    !seviye @kullanici
    ```
    veya
    ```bash
    !seviye
    ```

#### Ekonomi Komutları

- **Bakiye Gösterme**: Kullanıcının bakiyesini gösterir.
    ```bash
    !bakiye @kullanici
    ```
    veya
    ```bash
    !bakiye
    ```

- **Para Kazanma**: Kullanıcıya belirli miktarda para kazandırır.
    ```bash
    !earn
    ```

- **Coin Flip**: Belirtilen miktarda coin flip atar.
    ```bash
    !coinflip 50
    ```
    veya tüm bakiyenizle oynamak için:
    ```bash
    !coinflip all
    ```

- **Lider Tablosu**: En zengin kullanıcıları gösterir.
    ```bash
    !leaderboard
    ```

#### Botadmin Komutları

**Not:** Bu komutları kullanmak için bot yöneticisi olmanız gerekmektedir.

- **Bakiye Ayarlama**: Kullanıcının bakiyesini ayarlar.
    ```bash
    !set_bakiye @kullanici 1000
    ```

- **Seviye Ayarlama**: Kullanıcının seviyesini ve XP'sini ayarlar.
    ```bash
    !set_seviye @kullanici 5 250
    ```

- **Kullanıcı Verilerini Gösterme**: Kullanıcının verilerini gösterir.
    ```bash
    !get_user_data @kullanici
    ```

- **Kullanıcı Verilerini Ayarlama**: Kullanıcının verilerini ayarlar.
    ```bash
    !set_user_data @kullanici {"level": 3, "xp": 150, "balance": 500}
    ```

- **Bot Durumunu Değiştirme**: Botun durumunu değiştirir.
    ```bash
    !change_status Şu an eğleniyorum!
    ```

- **Hata Loglarını Gönderme**: Hata loglarını gönderir.
    ```bash
    !send_error_logs
    ```

#### Çekiliş Komutları

- **Çekiliş Oluşturma**: Belirtilen süre ve ödülle bir çekiliş oluşturur.
    ```bash
    !çekiliş_oluştur 1h 50$ ödülü
    ```

- **Çekiliş İptal Etme**: Belirtilen mesaj ID'sine sahip çekilişi iptal eder.
    ```bash
    !çekiliş_iptal 123456789012345678
    ```

## Hata Ayıklama

Bot çalışırken herhangi bir hata ile karşılaşırsanız, `error_logs.txt` dosyasını kontrol edebilirsiniz. Bu dosya, botun çalışması sırasında meydana gelen hataları kaydeder.

## Önemli bir not

Bot tek sunucu için tasarlanmış ve yazılmıştır. Botunuzun başka sunuculara girmesini önlemek için Discord Developer Portal'dan botunuzun Public Bot ayarının kapalı olduğundan emin olun.
