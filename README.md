# 📩 Avito → Telegram Notification Bot

Бот для автоматических уведомлений в Telegram о новых непрочитанных сообщениях в Avito.  
Работает через официальный Avito Messenger API и Telegram Bot API.

## 🚀 Возможности

- 📬 Уведомляет о каждом новом сообщении в Avito
- 🔄 Периодически опрашивает Avito API
- 🤖 Отправляет уведомления в Telegram
- 🔐 Все секреты хранятся в `.env`
- ♻️ Автоматически обновляет OAuth-токен Avito
- 🧠 Не отправляет дубликаты сообщений
- 🧹 Ограничивает историю чатов в памяти
- 📊 Команда `/status` показывает состояние бота

## ⚙️ Установка

1. Клонируйте репозиторий:

   ```bash
   git clone <repo-url>
   cd avito-notifications-telegram-bot
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Создайте `.env` на основе примера:

   ```bash
   cp .env.example .env
   ```

5. Заполните `.env` своими значениями.

## 🧩 Переменные окружения

| Переменная | Обязательна | Описание |
|---|---|---|
| `TELEGRAM_TOKEN` | ✅ | Токен Telegram-бота |
| `TELEGRAM_CHAT_ID` | ✅ | ID чата (или пользователя), куда отправлять уведомления |
| `AVITO_CLIENT_ID` | ✅ | Client ID из Avito API |
| `AVITO_CLIENT_SECRET` | ✅ | Client Secret из Avito API |
| `CHECK_INTERVAL` | ➖ | Интервал опроса Avito в секундах (по умолчанию `60`) |
| `HISTORY_LIMIT` | ➖ | Лимит кэша обработанных чатов (по умолчанию `3000`) |
| `LOG_LEVEL` | ➖ | Уровень логирования (`INFO`, `DEBUG`, `WARNING` и т.д.) |

## ▶️ Запуск

```bash
python bot.py
```

## 🤖 Команды Telegram

- `/start` — краткая справка по работе бота
- `/status` — текущий статус, интервал проверки и размер кэша
