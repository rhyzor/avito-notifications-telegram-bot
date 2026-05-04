# 📩 Avito → Ubuntu Notification Bot

Скрипт для уведомлений о новых непрочитанных сообщениях в Avito на Ubuntu:
- выводит сообщение в консоль,
- показывает desktop-уведомление через `notify-send`.
- основная фишка в том что у тебя на Авито бесконечный онлайн
- ранее бот присылал уведомления на телеграмм, но в связи с его блокировкой в рф я поменял на уведомления на Ubuntu для личного удобства
- Если вам нужно сделать бота под тг/винду/другую ос - напишите мне, буду рад помочь

Работает через официальный Avito Messenger API.

## 🚀 Возможности

- 📬 Уведомляет о каждом новом сообщении в Avito
- 🔄 Периодически опрашивает Avito API
- 🖥️ Показывает Ubuntu desktop notification (`notify-send`)
- 🧾 Дублирует уведомления в консоль
- 🔐 Все секреты хранятся в `.env`
- ♻️ Автоматически обновляет OAuth-токен Avito
- 🧠 Не отправляет дубликаты сообщений
- 🧹 Ограничивает историю чатов в памяти

## ⚙️ Установка

1. Установите системную зависимость для desktop-уведомлений:

```bash
sudo apt update
sudo apt install -y libnotify-bin
```

2. Подготовьте окружение Python:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Создайте `.env`:

```bash
cp .env.example .env
```

4. Заполните `.env` вашими данными Avito API.

## 🧩 Переменные окружения

| Переменная | Обязательна | Описание |
|---|---|---|
| `AVITO_CLIENT_ID` | ✅ | Client ID из Avito API |
| `AVITO_CLIENT_SECRET` | ✅ | Client Secret из Avito API |
| `CHECK_INTERVAL` | ➖ | Интервал опроса в секундах (по умолчанию `60`) |
| `HISTORY_LIMIT` | ➖ | Лимит кэша обработанных чатов (по умолчанию `3000`) |
| `LOG_LEVEL` | ➖ | Уровень логирования (`INFO`, `DEBUG`, `WARNING` и т.д.) |
| `ENABLE_DESKTOP_NOTIFY` | ➖ | `true/false`, включить уведомления Ubuntu (по умолчанию `true`) |

## ▶️ Запуск

```bash
python bot.py
```

## 📝 Что происходит при новом сообщении

1. Сообщение появляется в консоли.
2. Показывается уведомление Ubuntu через `notify-send`.

---

## ⭐ Поддержка / Связь

GitHub: [@rhyzor](https://github.com/rhyzor)

Telegram: [@rhyzor1](https://t.me/rhyzor1)
