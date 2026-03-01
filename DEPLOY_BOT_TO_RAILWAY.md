# Деплой Telegram бота на Railway.app

## Почему Railway?
- ✅ У вас уже есть база данных PostgreSQL на Railway
- ✅ 500 часов бесплатно в месяц (достаточно для бота)
- ✅ Автоматический деплой из GitHub
- ✅ Простая настройка
- ✅ Бот будет работать 24/7

## Шаг 1: Подготовка проекта

### 1.1 Создайте файл `requirements.txt` (если еще нет)
```txt
python-telegram-bot==20.7
psycopg2-binary==2.9.9
python-dotenv==1.0.0
openpyxl==3.1.2
```

### 1.2 Создайте файл `Procfile` в корне проекта
```
worker: python bot.py
```

### 1.3 Создайте файл `runtime.txt` (если еще нет)
```
python-3.11.7
```

### 1.4 Убедитесь, что `.env` в `.gitignore`
```
.env
__pycache__/
*.pyc
*.log
```

## Шаг 2: Загрузка на GitHub

### 2.1 Инициализируйте Git (если еще не сделано)
```bash
git init
git add .
git commit -m "Initial commit"
```

### 2.2 Создайте репозиторий на GitHub
1. Зайдите на https://github.com
2. Нажмите "New repository"
3. Назовите репозиторий (например, "telegram-bot")
4. Нажмите "Create repository"

### 2.3 Загрузите код на GitHub
```bash
git remote add origin https://github.com/ваш-username/telegram-bot.git
git branch -M main
git push -u origin main
```

## Шаг 3: Деплой на Railway

### 3.1 Зайдите на Railway.app
1. Откройте https://railway.app
2. Войдите через GitHub

### 3.2 Создайте новый проект
1. Нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Выберите ваш репозиторий с ботом

### 3.3 Настройте переменные окружения
В Railway проекте:
1. Откройте вкладку "Variables"
2. Добавьте переменные:
   - `BOT_TOKEN` = `8333299455:AAGVaSEmB7AHyDqTb2bY3kwQ0hnbx8iCC2s`
   - `DATABASE_URL` = `postgresql://postgres:BsZJFBgvpSAiOYdLjBTusBKqHDMFdbVs@nozomi.proxy.rlwy.net:30779/railway`

### 3.4 Настройте тип сервиса
1. В настройках проекта найдите "Service"
2. Убедитесь, что тип: "Worker" (не Web)
3. Railway автоматически найдет `Procfile`

### 3.5 Деплой
1. Railway автоматически начнет деплой
2. Дождитесь завершения (1-3 минуты)
3. Проверьте логи: вкладка "Deployments" → "View Logs"

## Шаг 4: Проверка работы

### 4.1 Проверьте логи
В Railway:
1. Откройте "Deployments"
2. Нажмите на последний деплой
3. Нажмите "View Logs"
4. Должны увидеть: "Bot started successfully" или подобное

### 4.2 Проверьте бота в Telegram
1. Откройте Telegram
2. Найдите вашего бота
3. Отправьте `/start`
4. Бот должен ответить

## Шаг 5: Мониторинг

### 5.1 Просмотр логов
```bash
# В Railway веб-интерфейсе
Deployments → View Logs
```

### 5.2 Перезапуск бота
```bash
# В Railway веб-интерфейсе
Settings → Restart
```

### 5.3 Остановка бота
```bash
# В Railway веб-интерфейсе
Settings → Remove Service
```

## Альтернатива: Деплой на Render.com

### Шаг 1: Подготовка
Те же файлы: `requirements.txt`, `Procfile`, `runtime.txt`

### Шаг 2: Создание сервиса
1. Зайдите на https://render.com
2. Нажмите "New +" → "Background Worker"
3. Подключите GitHub репозиторий
4. Настройте:
   - Name: telegram-bot
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`

### Шаг 3: Переменные окружения
Добавьте в Environment Variables:
- `BOT_TOKEN`
- `DATABASE_URL`

### Шаг 4: Деплой
Нажмите "Create Background Worker"

## Альтернатива: VPS сервер

### Если хотите использовать VPS:

#### 1. Подключитесь к серверу
```bash
ssh root@your-server-ip
```

#### 2. Установите Python и зависимости
```bash
apt update
apt install python3 python3-pip git
```

#### 3. Клонируйте проект
```bash
git clone https://github.com/ваш-username/telegram-bot.git
cd telegram-bot
```

#### 4. Установите зависимости
```bash
pip3 install -r requirements.txt
```

#### 5. Создайте .env файл
```bash
nano .env
```
Вставьте:
```
BOT_TOKEN=8333299455:AAGVaSEmB7AHyDqTb2bY3kwQ0hnbx8iCC2s
DATABASE_URL=postgresql://postgres:BsZJFBgvpSAiOYdLjBTusBKqHDMFdbVs@nozomi.proxy.rlwy.net:30779/railway
```

#### 6. Запустите бота в фоне
```bash
nohup python3 bot.py > bot.log 2>&1 &
```

#### 7. Проверьте работу
```bash
tail -f bot.log
```

#### 8. Автозапуск при перезагрузке (systemd)
Создайте файл `/etc/systemd/system/telegram-bot.service`:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/telegram-bot
ExecStart=/usr/bin/python3 /root/telegram-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активируйте:
```bash
systemctl enable telegram-bot
systemctl start telegram-bot
systemctl status telegram-bot
```

## Сравнение вариантов

| Вариант | Цена | Сложность | Надежность | Рекомендация |
|---------|------|-----------|------------|--------------|
| Railway.app | Бесплатно (500ч) | ⭐ Легко | ⭐⭐⭐ Высокая | ✅ Лучший выбор |
| Render.com | Бесплатно | ⭐ Легко | ⭐⭐⭐ Высокая | ✅ Хорошо |
| VPS | $2-5/мес | ⭐⭐ Средне | ⭐⭐⭐⭐ Очень высокая | ✅ Для опытных |
| Домашний ПК | Бесплатно | ⭐⭐⭐ Сложно | ⭐ Низкая | ❌ Не рекомендуется |

## Рекомендация

**Используйте Railway.app:**
1. У вас уже есть БД там
2. Бесплатно
3. Легко настроить
4. Работает 24/7
5. Автоматический деплой

## Мониторинг работы бота

### Проверка статуса
```python
# Добавьте в bot.py команду /status
@app.route('/status')
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Бот работает!')
```

### Уведомления об ошибках
Можно настроить отправку ошибок админу:
```python
async def error_handler(update, context):
    # Отправить ошибку админу
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f'❌ Ошибка: {context.error}'
    )
```

## Часто задаваемые вопросы

### Q: Сколько стоит Railway?
A: Бесплатно 500 часов в месяц. Для одного бота этого достаточно.

### Q: Что если 500 часов закончатся?
A: Можно перейти на платный план ($5/мес) или использовать другой сервис.

### Q: Можно ли запустить бота и веб-приложение вместе?
A: Да, но лучше разделить на два сервиса в Railway.

### Q: Как обновить бота?
A: Просто сделайте `git push` - Railway автоматически обновит.

### Q: Как посмотреть логи?
A: В Railway: Deployments → View Logs

### Q: Бот не отвечает, что делать?
A: Проверьте логи в Railway, возможно ошибка в коде или БД недоступна.

## Поддержка

Если возникнут проблемы:
1. Проверьте логи в Railway
2. Проверьте переменные окружения
3. Проверьте подключение к БД
4. Проверьте BOT_TOKEN

---

**Рекомендация:** Используйте Railway.app для простого и надежного хостинга бота 24/7!
