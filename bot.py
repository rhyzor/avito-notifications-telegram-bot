import logging
import os
import shutil
import subprocess
import time
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv

# ================== LOGGING ==================

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ================== LOAD ENV ==================

load_dotenv()

AVITO_CLIENT_ID = os.getenv("AVITO_CLIENT_ID")
AVITO_CLIENT_SECRET = os.getenv("AVITO_CLIENT_SECRET")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))
HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT", 3000))
ENABLE_DESKTOP_NOTIFY = os.getenv("ENABLE_DESKTOP_NOTIFY", "true").lower() == "true"

if not all([AVITO_CLIENT_ID, AVITO_CLIENT_SECRET]):
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


LAST_UPDATED: dict[str, int] = {}


def _safe_timestamp(chat: dict[str, Any]) -> int:
    raw_value = chat.get("updated") or chat.get("created") or 0
    try:
        return int(raw_value)
    except (ValueError, TypeError):
        return 0


def _cleanup_history() -> None:
    if len(LAST_UPDATED) <= HISTORY_LIMIT:
        return

    overflow = len(LAST_UPDATED) - HISTORY_LIMIT
    for chat_id in list(LAST_UPDATED)[:overflow]:
        LAST_UPDATED.pop(chat_id, None)


def send_ubuntu_notification(title: str, message: str) -> None:
    """Показывает локальное уведомление в Ubuntu через notify-send."""
    if not ENABLE_DESKTOP_NOTIFY:
        return

    if shutil.which("notify-send") is None:
        logger.warning("Команда notify-send не найдена. Установите libnotify-bin.")
        return

    try:
        subprocess.run(["notify-send", title, message], check=False)
    except Exception:
        logger.exception("Не удалось отправить desktop notification")


def notify_new_message(chat: dict[str, Any]) -> None:
    title = chat.get("context", {}).get("value", {}).get("title", "Без названия")
    chat_id = chat.get("id", "unknown")
    updated_ts = _safe_timestamp(chat)

    when = datetime.fromtimestamp(updated_ts).strftime("%d.%m %H:%M") if updated_ts > 0 else "unknown time"

    text = f"📩 Новое сообщение в Avito | Чат: {chat_id} | Объявление: {title} | Время: {when}"

    # Console message
    logger.info(text)
    print(text)

    # Ubuntu desktop notification
    send_ubuntu_notification("Новое сообщение Avito", f"{title}\n{when}")


def poll_avito() -> None:
    logger.info("Запущен цикл проверки Avito (каждые %s сек.)", CHECK_INTERVAL)

    while True:
        try:
            chats = get_unread_chats()

            for chat in chats:
                chat_id = chat.get("id")
                if not isinstance(chat_id, str):
                    continue

                if chat_id.startswith(("seller_", "flower_", "sbc_")):
                    continue

                updated_ts = _safe_timestamp(chat)
                if updated_ts <= 0:
                    continue

                last_ts = LAST_UPDATED.get(chat_id, 0)
                if updated_ts <= last_ts:
                    continue

                LAST_UPDATED[chat_id] = updated_ts
                notify_new_message(chat)

            _cleanup_history()

        except Exception:
            logger.exception("🔥 Ошибка в цикле опроса")

        time.sleep(CHECK_INTERVAL)


def main() -> None:
    global AVITO_USER_ID

    AVITO_USER_ID = get_avito_user_id()
    logger.info("👤 Avito user_id: %s", AVITO_USER_ID)

    poll_avito()


if __name__ == "__main__":
    main()
