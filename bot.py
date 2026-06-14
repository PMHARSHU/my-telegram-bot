import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp

# --- ADVANCED LOGGING SETUP ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- CREDENTIALS (CONFIG) ---
API_ID = 35087613
API_HASH = "b5e83c700155faf98bb6b95c05abaafd"
BOT_TOKEN = "8898617678:AAEoFs1E1vbFcqkvNNchGvyhvCU3APtbE2w"

# --- INITIALIZING CLIENT ---
app = Client(
    "harsh_advanced_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- STARTUP MESSAGE HANDLER ---
async def start_bot_announcement():
    print("\n" + "="*50)
    print("🚀 BOT START SUCCESSFULLY IN TERMUX!")
    print("🤖 BOT BOLO: MEIN EK ADVANCED TELEGRAM BOT HU!")
    print("🚩 JAI SHREE RAM, HARSH BHAI!")
    print("="*50 + "\n")
    logger.info("Advanced Media Downloader Bot is now online.")

# --- COMMANDS & HANDLERS ---

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        "**Jai Shree Ram, HARSH bhai! 🚩**\n\n"
        "🤖 **Bot Status:** Active & Advanced\n\n"
        "Mujhe kisi bhi Instagram Reel, YouTube Short, ya video ka link bhejo. "
        "Mein use background mein process karke direct file aapko bhej dunga!"
    )

@app.on_message(filters.regex(r"https?://(www\.)?(instagram\.com|youtube\.com|youtu\.be|shorts)/.+") & filters.private)
async def media_downloader(client: Client, message: Message):
    url = message.text
    status_msg = await message.reply_text("🔎 **Link detect ho gaya hai... Verifying...**")
    
    # Dynamic Unique Filename
    file_name = f"download_{message.from_user.id}_{message.id}.mp4"
    
    ydl_opts = {
        'outtmpl': file_name,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        await status_msg.edit_text("📥 **Downloading... Please wait, process advanced framework par chal raha hai.**")
        
        # Non-blocking async execution for yt-dlp
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await loop.run_in_executor(None, lambda: ydl.download([url]))
            
        if not os.path.exists(file_name):
            await status_msg.edit_text("❌ **Error:** Video download nahi ho saki. Link checking failed.")
            return
            
        await status_msg.edit_text("📤 **Uploading file to Telegram cloud...**")
        
        # Sending video with streaming support
        await message.reply_video(
            video=file_name,
            caption=f"✨ **Aapki Video Ready Hai!**\n\n⚡ _Powered by Harsh's Advanced Bot_",
            supports_streaming=True
        )
        await status_msg.delete()
        
    except Exception as e:
        logger.error(f"Error while processing link: {e}")
        await status_msg.edit_text(f"❌ **An error occurred:** `{str(e)}`")
        
    finally:
        # Memory Cleanup (Server space free rakhne ke liye)
        if os.path.exists(file_name):
            os.remove(file_name)

# --- RUNNING THE BOT WITH ADVANCED WRAPPER ---
if __name__ == "__main__":
    try:
        app.start()
        # Custom console messages run karna startup par
        app.loop.run_until_complete(start_bot_announcement())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped safely by Harsh.")
    except Exception as err:
        logger.critical(f"Bot crashed: {err}")

