import time
import asyncio
import requests
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ================== НАСТРОЙКИ ==================

# --- TELEGRAM ---
TELEGRAM_TOKEN = "PUT_TELEGRAM_TOKEN_HERE"
TELEGRAM_CHAT_ID = "PUT_TELEGRAM_CHAT_ID_HERE"

# --- AVITO ---
AVITO_CLIENT_ID = "PUT_CLIENT_ID_HERE"
AVITO_CLIENT_SECRET = "PUT_CLIENT_SECRET_HERE"

CHECK_INTERVAL = 60  # секунд

# ================== AVITO TOKEN ==================

_avito_token = None
_avito_token_expires = 0
AVITO_USER_ID = None


def get_avito_token():
    global _avito_token, _avito_token_expires

    if _avito_token and time.time() < _avito_token_expires:
        return _avito_token

    r = requests.post(
        "https://api.avito.ru/token",
        data={
            "grant_type": "client_credentials",
            "client_id": AVITO_CLIENT_ID,
            "client_secret": AVITO_CLIENT_SECRET,
            "scope": "messenger:read",
        },
        timeout=10,
    )

    data = r.json()
    if "access_token" not in data:
        raise RuntimeError(f"Avito token error: {data}")

    _avito_token = data["access_token"]
    _avito_token_expires = time.time() + data.get("expires_in", 3600) - 60

    print("🔐 Avito token обновлён")
    return _avito_token


def avito_request(method, url, **kwargs):
    token = get_avito_token()

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {token}"

    r = requests.request(method, url, headers=headers, **kwargs)

    if not r.ok:
        print("❌ Avito error:", r.status_code, r.text)

    r.raise_for_status()
    return r


# ================== AVITO USER ID ==================

def get_avito_user_id():
    r = avito_request("GET", "https://api.avito.ru/core/v1/accounts/self")
    return r.json()["id"]


# ================== AVITO API ==================

def get_unread_chats():
    url = f"https://api.avito.ru/messenger/v2/accounts/{AVITO_USER_ID}/chats"
    params = {
        "unread_only": "true",
        "limit": 50,
        "chat_types": "u2i",
    }
    r = avito_request("GET", url, params=params)
    return r.json().get("chats", [])


# ================== TELEGRAM ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Бот запущен.\n"
        "Уведомления будут приходить при каждом новом сообщении в Avito."
    )


# ================== ОСНОВНОЙ ЦИКЛ ==================

LAST_UPDATED = {}  # chat_id -> timestamp


async def poll_avito(app):
    while True:
        try:
            chats = get_unread_chats()

            for chat in chats:
                chat_id = chat["id"]

                # ❌ системные / бот-чаты
                if chat_id.startswith(("seller_", "flower_", "sbc_")):
                    continue

                updated_ts = chat.get("updated") or chat.get("created", 0)
                last_ts = LAST_UPDATED.get(chat_id, 0)

                # ❗ если новых сообщений нет — пропускаем
                if updated_ts <= last_ts:
                    continue

                LAST_UPDATED[chat_id] = updated_ts

                title = (
                    chat.get("context", {})
                    .get("value", {})
                    .get("title", "Без названия")
                )

                ts = datetime.fromtimestamp(updated_ts).strftime("%d.%m %H:%M")

                await app.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=(
                        "📩 *Новое сообщение в Avito*\n\n"
                        f"📦 {title}\n"
                        f"🕒 {ts}\n\n"
                        "👉 Откройте чат в Avito"
                    ),
                    parse_mode="Markdown",
                )

        except Exception as e:
            print("🔥 Ошибка:", e)

        await asyncio.sleep(CHECK_INTERVAL)


# ================== ЗАПУСК ==================

async def main():
    global AVITO_USER_ID

    AVITO_USER_ID = get_avito_user_id()
    print("👤 Avito user_id:", AVITO_USER_ID)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    await app.initialize()
    await app.start()

    me = await app.bot.get_me()
    print("🤖 Telegram bot:", me.username)

    await poll_avito(app)


if __name__ == "__main__":
    asyncio.run(main())
