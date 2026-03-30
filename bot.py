import asyncio
import logging
import os
import time
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ================== LOGGING ==================

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ================== LOAD ENV ==================

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

AVITO_CLIENT_ID = os.getenv("AVITO_CLIENT_ID")
AVITO_CLIENT_SECRET = os.getenv("AVITO_CLIENT_SECRET")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))
HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT", 3000))

if not all([
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
    AVITO_CLIENT_ID,
    AVITO_CLIENT_SECRET,
]):
    raise RuntimeError("❌ Не все переменные окружения заданы в .env")


# ================== AVITO TOKEN ==================

_avito_token: str | None = None
_avito_token_expires = 0.0
AVITO_USER_ID: int | None = None


def get_avito_token() -> str:
    global _avito_token, _avito_token_expires

    if _avito_token and time.time() < _avito_token_expires:
        return _avito_token

    response = requests.post(
        "https://api.avito.ru/token",
        data={
            "grant_type": "client_credentials",
            "client_id": AVITO_CLIENT_ID,
            "client_secret": AVITO_CLIENT_SECRET,
            "scope": "messenger:read",
        },
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()
    if "access_token" not in data:
        raise RuntimeError(f"Avito token error: {data}")

    _avito_token = data["access_token"]
    _avito_token_expires = time.time() + data.get("expires_in", 3600) - 60

    logger.info("🔐 Avito token обновлён")
    return _avito_token


def avito_request(method: str, url: str, **kwargs: Any) -> requests.Response:
    token = get_avito_token()

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {token}"

    response = requests.request(method, url, headers=headers, timeout=15, **kwargs)

    if not response.ok:
        logger.error("❌ Avito error: %s %s", response.status_code, response.text)

    response.raise_for_status()
    return response


# ================== AVITO API ==================

def get_avito_user_id() -> int:
    response = avito_request("GET", "https://api.avito.ru/core/v1/accounts/self")
    return int(response.json()["id"])


def get_unread_chats() -> list[dict[str, Any]]:
    url = f"https://api.avito.ru/messenger/v2/accounts/{AVITO_USER_ID}/chats"
    params = {
        "unread_only": "true",
        "limit": 50,
        "chat_types": "u2i",
    }
    response = avito_request("GET", url, params=params)
    return response.json().get("chats", [])


# ================== TELEGRAM ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤖 Бот запущен.\n"
        "Уведомления будут приходить при каждом новом сообщении в Avito."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "✅ Бот работает.\n"
        f"Интервал проверки: {CHECK_INTERVAL} сек.\n"
        f"История чатов в памяти: {len(LAST_UPDATED)}"
    )


# ================== ОСНОВНОЙ ЦИКЛ ==================

LAST_UPDATED: dict[str, int] = {}


def _safe_timestamp(chat: dict[str, Any]) -> int:
    raw_value = chat.get("updated") or chat.get("created") or 0
    try:
        return int(raw_value)
    except (ValueError, TypeError):
        return 0


def _cleanup_history() -> None:
    """Ограничивает размер истории, чтобы память не росла бесконечно."""
    if len(LAST_UPDATED) <= HISTORY_LIMIT:
        return

    overflow = len(LAST_UPDATED) - HISTORY_LIMIT
    for chat_id in list(LAST_UPDATED)[:overflow]:
        LAST_UPDATED.pop(chat_id, None)


async def poll_avito(app) -> None:
    while True:
        try:
            chats = get_unread_chats()

            for chat in chats:
                chat_id = chat.get("id")
                if not isinstance(chat_id, str):
                    continue

                # ❌ системные / бот-чаты
                if chat_id.startswith(("seller_", "flower_", "sbc_")):
                    continue

                updated_ts = _safe_timestamp(chat)
                if updated_ts <= 0:
                    continue

                last_ts = LAST_UPDATED.get(chat_id, 0)
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

            _cleanup_history()

        except Exception:
            logger.exception("🔥 Ошибка в цикле опроса")

        await asyncio.sleep(CHECK_INTERVAL)


# ================== ЗАПУСК ==================

async def main() -> None:
    global AVITO_USER_ID

    AVITO_USER_ID = get_avito_user_id()
    logger.info("👤 Avito user_id: %s", AVITO_USER_ID)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    await app.initialize()
    await app.start()

    me = await app.bot.get_me()
    logger.info("🤖 Telegram bot: %s", me.username)

    try:
        await poll_avito(app)
    finally:
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
