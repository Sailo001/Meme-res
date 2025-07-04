main.pyimport sys
import os
import json
import base58
import filetype
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.keypair import Keypair
from solana.system_program import TransferParams, transfer

# === CONFIG ===
BOT_TOKEN       = os.environ.get("BOT_TOKEN", "7967104380:AAExZF80A2yo4Zmhnjker1g46KDz-eX66PE")
PRIVATE_KEY     = os.environ.get("PRIVATE_KEY", "4R7Zz9veny77mvu8TJCBGdKFTtzswXgh6rS2YdbYKt5ZLhwHwJjVu2gYXLaTDERjPUsCpNaakUG428DL8rF28pxt")
SOLANA_RPC_URL  = os.environ.get("SOLANA_RPC_URL", "https://mainnet.helius-rpc.com/?api-key=0e6a2dae-dc80-4fa2-89e6-ad3ffc3b8e7c")
WEBHOOK_URL     = os.environ.get("WEBHOOK_URL", "https://meme-coin-awakener.onrender.com")

# === INIT ===
app             = Flask(__name__)
bot             = Bot(token=BOT_TOKEN)
dispatcher      = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)
solana_client   = Client(SOLANA_RPC_URL)

# --- Keypair Handling ---
def load_keypair(private_key):
    try:
        try:
            return Keypair.from_secret_key(base58.b58decode(private_key))
        except Exception:
            if private_key.startswith('['):
                arr = json.loads(private_key)
            else:
                arr = list(map(int, private_key.strip().split(",")))
            return Keypair.from_secret_key(bytes(arr))
    except Exception as e:
        print(f"Keypair load error: {e}")
        return None

keypair = load_keypair(PRIVATE_KEY)

# === COMMAND HANDLERS ===
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("📈 Boost Volume", callback_data="boost")],
        [InlineKeyboardButton("📊 Stats",       callback_data="stats")],
        [InlineKeyboardButton("🛑 Stop",        callback_data="stop")]
    ]
    update.message.reply_text(
        "🚀 Welcome to Meme Coin Awakener!\nSelect an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button_callback(update, context):
    query = update.callback_query
    data  = query.data
    query.answer()

    if data == "boost":
        query.edit_message_text("🔄 Boosting volume with real transaction...")
        simulate_transaction()
    elif data == "stats":
        query.edit_message_text("📊 Token Stats:\n• Price: 0.001 SOL\n• Volume: 10,000")
    elif data == "stop":
        query.edit_message_text("⛔ Booster stopped.")

# === SOLANA TX ===
def simulate_transaction():
    if keypair is None:
        print("No keypair loaded, cannot send transaction.")
        return
    try:
        target_pubkey = keypair.public_key
        tx = Transaction()
        tx.add(transfer(TransferParams(
            from_pubkey=keypair.public_key,
            to_pubkey=target_pubkey,
            lamports=1000
        )))
        recent_blockhash = solana_client.get_recent_blockhash()["result"]["value"]["blockhash"]
        tx.recent_blockhash = recent_blockhash
        tx.sign(keypair)
        res = solana_client.send_raw_transaction(tx.serialize())
        print(f"Transaction sent: {res}")
    except Exception as e:
        print(f"Transaction failed: {e}")

# === FLASK WEBHOOK ===
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Meme Coin Awakener Bot is Live"

def main():
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
PK     Z_�Z�s��U   U      requirements.txtpython-telegram-bot==13.15
Flask==2.3.3
solana==0.31.0
base58==2.1.1
filetype==1.2.0
PK     Z_�Z�&>E  E  	   README.md# Meme Coin Awakener Bot

A Telegram bot that interacts with Solana to simulate volume-boosting transactions for meme tokens.

## Deployment

Deploy this on Render using:
- Python build environment
- Start command: `python main.py`
- Set the environment variables: `BOT_TOKEN`, `PRIVATE_KEY`, `SOLANA_RPC_URL`, `WEBHOOK_URL`
PK     Z_�Z�9��5  5             ��    main.pyPK     Z_�Z�s��U   U              ��Z  requirements.txtPK     Z_�Z�&>E  E  	           ���  README.mdPK      �   I    
