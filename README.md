
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
- 💻 Работает на Windows, Linux, VPS

## ⚡ Быстрый старт

```bash
git clone https://github.com/yourusername/avito-telegram-bot.git
cd avito-telegram-bot
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
cp .env.example .env  # заполните своими данными
python bot.py
```

## 🔧 Требования

- Python 3.9+ (рекомендуется 3.10 или 3.11)
- Аккаунт Avito с доступом к [API](https://api.avito.ru/)
- Telegram-бот, созданный через [@BotFather](https://t.me/BotFather)

## 📦 Установка

### 1️⃣ Клонируйте или создайте папку проекта

```bash
mkdir avito_bot
cd avito_bot
```

### 2️⃣ Создайте виртуальное окружение

```bash
python -m venv venv
```

**Активация:**

Windows:
```bash
venv\Scripts\activate
```

Linux / macOS:
```bash
source venv/bin/activate
```

### 3️⃣ Установите зависимости

```bash
pip install -r requirements.txt
```

**Содержимое requirements.txt:**
```
requests>=2.31
python-telegram-bot>=20,<21
python-dotenv>=1.0
```

## 🔐 Настройка `.env`

Создайте файл `.env` в корне проекта:

```env
# Telegram
TELEGRAM_TOKEN=123456789:AAAbbbCCCdddEEE
TELEGRAM_CHAT_ID=123456789

# Avito API
AVITO_CLIENT_ID=your_client_id
AVITO_CLIENT_SECRET=your_client_secret

# Интервал проверки (секунды)
CHECK_INTERVAL=60
```

### Как получить данные:

- **TELEGRAM_TOKEN**: создайте бота через [@BotFather](https://t.me/BotFather)
- **TELEGRAM_CHAT_ID**: отправьте любое сообщение боту, затем перейдите по ссылке:  
  `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` — найдите `chat.id`
- **AVITO_CLIENT_ID / SECRET**:  
  1. Перейдите в [Avito API](https://api.avito.ru/)
  2. Создайте приложение
  3. В разделе "OAuth" получите Client ID и Client Secret

## ▶️ Запуск

```bash
python bot.py
```

При успешном запуске увидите:
```
👤 Avito user_id: 123456789
🤖 Telegram bot: YourBotName
```

В Telegram бот ответит на команду `/start`.

## 🧠 Как это работает

1. Получает OAuth-токен Avito
2. Узнаёт `user_id` аккаунта
3. Каждые `CHECK_INTERVAL` секунд:
   - запрашивает непрочитанные чаты
   - фильтрует системные диалоги
   - проверяет наличие новых сообщений
4. Отправляет уведомление в Telegram
5. Запоминает последний timestamp для предотвращения дубликатов

## 🛡 Безопасность

- Все токены хранятся в `.env`, который **не попадает в репозиторий**
- Рекомендуется добавить `.env` в `.gitignore`
- При необходимости можно обновлять `.env` без перезапуска кода

## 📁 `.gitignore` (рекомендуемый)

```
.env
venv/
__pycache__/
*.pyc
.DS_Store
```

## 🖥 Автозапуск

### Windows (Планировщик заданий)
Создайте задачу для запуска `python bot.py` при старте системы.

### Linux / VPS (systemd)
Создайте файл `/etc/systemd/system/avito-bot.service`:
```ini
[Unit]
Description=Avito Telegram Bot
After=network.target

[Service]
User=youruser
WorkingDirectory=/path/to/avito_bot
ExecStart=/path/to/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Затем выполните:
```bash
sudo systemctl enable avito-bot
sudo systemctl start avito-bot
```

## 🧪 Отладка и логи

При ошибках в консоль выводится:
```
❌ Avito error: 401 Unauthorized
🔥 Ошибка: ...
```

Для production рекомендуется настроить:
- Логирование в файл
- Уведомления об ошибках в Telegram
- Retry-механизм с backoff

## 📌 Ограничения

- Используется polling (не webhook)
- Работает только с личными чатами (`u2i`)
- Зависит от лимитов Avito API

## 🧩 Идеи для улучшения

- [ ] Логирование в файл
- [ ] Уведомления при ошибках
- [ ] Retry при 5xx ошибках
- [ ] Статистика сообщений
- [ ] Unit-тесты
- [ ] Docker-образ

## 🤝 Вклад в проект

PR и issues приветствуются.  
Перед отправкой изменений:
1. Убедитесь, что код работает с вашими данными
2. Проверьте на наличие лишних отладочных выводов
3. Обновите README при необходимости

## 📄 Лицензия

MIT License. Используйте свободно, но с указанием авторства.

## 📬 Поддержка

Если возникли проблемы:
1. Проверьте корректность `.env`
2. Убедитесь, что Avito API доступен
3. Проверьте версии библиотек: `pip list`
4. Посмотрите вывод в консоли
