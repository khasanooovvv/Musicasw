
import os
import telebot
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

# Tokenlarni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram botni yaratish
bot = telebot.TeleBot(BOT_TOKEN)

# Musiqa yuklab olish funksiyasi
def download_audio(search_query):
    options = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(f"ytsearch:{search_query}", download=True)
        file_path = ydl.prepare_filename(info["entries"][0]).replace(".webm", ".mp3")
    return file_path

# Start va yordam xabari
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Salom! Musiqa nomini yozing, men sizga faylni yuboraman.")

# Musiqa qidirish va yuklab olish
@bot.message_handler(func=lambda message: True)
def send_music(message):
    query = message.text
    bot.reply_to(message, f"'{query}' musiqasini qidiryapman...")
    
    try:
        # Musiqani yuklab olish
        file_path = download_audio(query)
        with open(file_path, "rb") as audio:
            bot.send_audio(message.chat.id, audio)
        
        # Faylni o'chirish
        os.remove(file_path)
    except Exception as e:
        bot.reply_to(message, "Kechirasiz, musiqani yuklab olishda xatolik yuz berdi.")

# Botni ishga tushirish
bot.infinity_polling()
