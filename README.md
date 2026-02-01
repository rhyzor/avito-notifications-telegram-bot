Конечно 🙂 Ниже — **подробный README.md**, уже в готовом виде.
Можно **целиком скопировать** и сохранить как `README.md` рядом с `bot.py`.

---

# 📩 Avito → Telegram Notification Bot

Бот для автоматических уведомлений в **Telegram** о **новых непрочитанных сообщениях в Avito**.
Работает через **официальный Avito API** и **Telegram Bot API**.

---

## 🚀 Возможности

* 📬 Уведомляет о **каждом новом сообщении в Avito**
* 🔄 Периодически опрашивает Avito API
* 🤖 Отправляет уведомления в Telegram
* 🔐 Все секреты хранятся в `.env` (безопасно)
* ♻️ Автоматически обновляет OAuth-токен Avito
* 🧠 Не шлёт дубликаты сообщений
* 💻 Работает на Windows / Linux / VPS

---

## 🧩 Используемые технологии

* Python 3.9+
* `python-telegram-bot` (async, v20+)
* `requests`
* `python-dotenv`
* Avito Messenger API

---

## 📂 Структура проекта

```text
avito_bot/
├─ bot.py               # основной код бота
├─ .env                 # секреты (НЕ коммитить)
├─ requirements.txt     # зависимости
├─ README.md            # документация
└─ venv/                # виртуальное окружение
```

---

## ⚙️ Требования

* Python **3.9 или выше** (рекомендуется 3.10 / 3.11)
* Аккаунт Avito с доступом к API
* Созданный Telegram-бот (@BotFather)

Проверка Python:

```bash
python --version
```

---

## 📦 Установка

### 1️⃣ Клонируй или создай папку проекта

```bash
mkdir avito_bot
cd avito_bot
```

---

### 2️⃣ Создай виртуальное окружение

```bash
python -m venv venv
```

Активация:

**Windows**

```bat
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### 3️⃣ Установи зависимости

```bash
pip install -r requirements.txt
```

**Содержимое `requirements.txt`:**

```txt
requests>=2.31
python-telegram-bot>=20,<21
python-dotenv>=1.0
```

---

## 🔐 Настройка `.env`

Создай файл **`.env`** в корне проекта:

```env
TELEGRAM_TOKEN=123456789:AAAbbbCCCdddEEE
TELEGRAM_CHAT_ID=123456789

AVITO_CLIENT_ID=your_avito_client_id
AVITO_CLIENT_SECRET=your_avito_client_secret

CHECK_INTERVAL=60
```

### 📌 Пояснения:

* `TELEGRAM_TOKEN` — токен бота от @BotFather
* `TELEGRAM_CHAT_ID` — ID чата или пользователя
* `AVITO_CLIENT_ID / SECRET` — из Avito API
* `CHECK_INTERVAL` — интервал проверки Avito (в секундах)

⚠️ **Важно**

* Без кавычек
* `.env` **не выкладывать в git**
* Chat ID — числом

---

## ▶️ Запуск бота

```bash
python bot.py
```

При успешном запуске ты увидишь:

```text
👤 Avito user_id: XXXXX
🤖 Telegram bot: your_bot_name
```

В Telegram:

```
/start
```

---

## 🧠 Как работает бот

1. Получает OAuth-токен Avito
2. Узнаёт `user_id` аккаунта
3. Каждые `CHECK_INTERVAL` секунд:

   * запрашивает непрочитанные чаты
   * фильтрует системные диалоги
   * проверяет, есть ли новые сообщения
4. Отправляет уведомление в Telegram
5. Запоминает последний timestamp, чтобы избежать дублей

---

## 🛡 Безопасность

* ❌ Токены не хранятся в коде
* ✅ `.env` можно менять без перезапуска кода
* 🔐 Готово для деплоя на сервер

Рекомендуется добавить `.gitignore`:

```gitignore
.env
venv/
__pycache__/
```

---

## 🖥 Автозапуск

Бот можно запускать:

* 🪟 через **Планировщик заданий Windows**
* 🐧 через **systemd** (Linux / VPS)
* 🐳 в Docker (при необходимости)

(настройки описываются отдельно)

---

## 🧪 Отладка и логи

Все ошибки выводятся в stdout:

```text
❌ Avito error: 401 ...
🔥 Ошибка: ...
```

При желании можно:

* добавить логирование в файл
* отправлять алерт в Telegram при падении
* добавить retry + backoff

---

## 📌 Ограничения

* Используется polling (не webhook)
* Зависит от лимитов Avito API
* Работает только с личными чатами (`u2i`)

---

## 🧩 Идеи для улучшения

* 📄 Логи в файл
* 🚨 Уведомление при ошибках
* 🔁 Retry при 5xx
* 📊 Статистика сообщений
* 🧪 Unit-тесты
* 🐳 Docker

---

## 📬 Поддержка

Если бот не запускается:

1. Проверь `.env`
2. Проверь версии библиотек
3. Убедись, что Avito API доступен
4. Посмотри вывод в консоли
