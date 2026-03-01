# Инструкция по деплою бота на Railway.app

## ✅ Ваш проект уже готов к деплою!

Все необходимые файлы на месте:
- ✅ `Procfile` - команда запуска бота
- ✅ `runtime.txt` - версия Python
- ✅ `requirements.txt` - зависимости
- ✅ `.gitignore` - исключает .env из Git
- ✅ `bot.py` - код бота
- ✅ База данных уже на Railway!

## Шаг 1: Подготовка GitHub репозитория

### 1.1 Инициализируйте Git (если еще не сделано)
```bash
git init
git add .
git commit -m "Prepare for Railway deployment"
```

### 1.2 Создайте репозиторий на GitHub
1. Откройте https://github.com
2. Войдите в свой аккаунт
3. Нажмите зеленую кнопку "New" (или "New repository")
4. Заполните:
   - Repository name: `telegram-warehouse-bot` (или любое имя)
   - Description: `Telegram bot for warehouse management`
   - Выберите: **Private** (чтобы скрыть код)
5. НЕ добавляйте README, .gitignore, license (у вас уже есть)
6. Нажмите "Create repository"

### 1.3 Загрузите код на GitHub
GitHub покажет команды, выполните их:
```bash
git remote add origin https://github.com/ваш-username/telegram-warehouse-bot.git
git branch -M main
git push -u origin main
```

**Важно:** Замените `ваш-username` на ваш реальный username на GitHub!

## Шаг 2: Деплой на Railway.app

### 2.1 Войдите на Railway
1. Откройте https://railway.app
2. Нажмите "Login"
3. Войдите через GitHub (рекомендуется)

### 2.2 Создайте новый проект
1. На главной странице Railway нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Если это первый раз:
   - Нажмите "Configure GitHub App"
   - Разрешите доступ к вашему репозиторию
4. Выберите репозиторий `telegram-warehouse-bot`
5. Railway начнет автоматический деплой

### 2.3 Настройте переменные окружения
Это самый важный шаг!

1. В Railway проекте откройте вкладку **"Variables"** (слева в меню)
2. Нажмите "New Variable"
3. Добавьте две переменные:

**Переменная 1:**
- Name: `BOT_TOKEN`
- Value: `8333299455:AAGVaSEmB7AHyDqTb2bY3kwQ0hnbx8iCC2s`

**Переменная 2:**
- Name: `DATABASE_URL`
- Value: `postgresql://postgres:BsZJFBgvpSAiOYdLjBTusBKqHDMFdbVs@nozomi.proxy.rlwy.net:30779/railway`

4. Нажмите "Add" для каждой переменной

### 2.4 Проверьте настройки
1. Откройте вкладку **"Settings"**
2. Убедитесь:
   - Service Name: `telegram-warehouse-bot` (или как назвали)
   - Builder: Nixpacks (автоматически)
   - Start Command: `python bot.py` (из Procfile)

### 2.5 Дождитесь завершения деплоя
1. Откройте вкладку **"Deployments"**
2. Вы увидите процесс деплоя
3. Статусы:
   - 🟡 Building... (1-2 минуты)
   - 🟡 Deploying...
   - 🟢 Success! (бот запущен)

## Шаг 3: Проверка работы бота

### 3.1 Проверьте логи
1. В Railway откройте вкладку **"Deployments"**
2. Нажмите на последний деплой (зеленая галочка)
3. Нажмите **"View Logs"**
4. Вы должны увидеть что-то вроде:
   ```
   Starting bot...
   Bot started successfully
   ```

### 3.2 Проверьте бота в Telegram
1. Откройте Telegram
2. Найдите вашего бота (по имени или @username)
3. Отправьте команду: `/start`
4. Бот должен ответить меню

### 3.3 Проверьте основные функции
Попробуйте:
- `/start` - главное меню
- Добавить приход
- Посмотреть остатки
- Добавить расход

## Шаг 4: Мониторинг и управление

### Просмотр логов в реальном времени
1. Railway → Deployments → View Logs
2. Логи обновляются автоматически

### Перезапуск бота
Если нужно перезапустить:
1. Railway → Settings
2. Нажмите "Restart"
3. Или просто сделайте новый `git push`

### Остановка бота
Если нужно остановить:
1. Railway → Settings
2. Прокрутите вниз
3. Нажмите "Remove Service"

### Обновление бота
Когда вы изменили код:
```bash
git add .
git commit -m "Update bot"
git push
```
Railway автоматически обновит бота!

## Шаг 5: Проверка использования ресурсов

### Бесплатный план Railway
- ✅ 500 часов в месяц
- ✅ $5 кредитов в месяц
- ✅ Достаточно для одного бота 24/7

### Проверка использования
1. Railway → Project Settings
2. Вкладка "Usage"
3. Смотрите:
   - Execution Time (часы работы)
   - Credits Used (использованные кредиты)

### Если закончатся бесплатные часы
Варианты:
1. Перейти на платный план ($5/месяц)
2. Создать новый аккаунт Railway
3. Перенести на другой сервис (Render.com)

## Возможные проблемы и решения

### ❌ Проблема: "Build failed"
**Решение:**
1. Проверьте `requirements.txt` - все зависимости указаны?
2. Проверьте `runtime.txt` - правильная версия Python?
3. Посмотрите логи билда для деталей

### ❌ Проблема: "Bot not responding"
**Решение:**
1. Проверьте логи: есть ли ошибки?
2. Проверьте переменные: BOT_TOKEN и DATABASE_URL правильные?
3. Проверьте подключение к БД: может быть БД недоступна?

### ❌ Проблема: "Database connection error"
**Решение:**
1. Проверьте DATABASE_URL в переменных
2. Убедитесь, что БД на Railway работает
3. Проверьте, что IP Railway не заблокирован в БД

### ❌ Проблема: "Module not found"
**Решение:**
1. Добавьте недостающий модуль в `requirements.txt`
2. Сделайте `git push` для обновления

## Дополнительные настройки

### Автоматическое резервное копирование БД
1. Railway → Database → Settings
2. Включите "Automated Backups"
3. Выберите частоту (ежедневно рекомендуется)

### Уведомления о проблемах
1. Railway → Project Settings → Notifications
2. Включите уведомления на email
3. Вы получите письмо, если бот упадет

### Мониторинг uptime
Используйте сервисы:
- UptimeRobot.com (бесплатно)
- Pingdom.com
- StatusCake.com

## Команды для управления

### Локальное тестирование перед деплоем
```bash
# Установите зависимости
pip install -r requirements.txt

# Запустите бота локально
python bot.py

# Проверьте, что все работает
# Затем делайте git push
```

### Просмотр статуса на Railway
```bash
# Установите Railway CLI (опционально)
npm i -g @railway/cli

# Войдите
railway login

# Просмотр логов
railway logs

# Перезапуск
railway restart
```

## Структура проекта на Railway

```
Railway Project
├── Service: telegram-warehouse-bot (ваш бот)
│   ├── Variables (BOT_TOKEN, DATABASE_URL)
│   ├── Deployments (история деплоев)
│   └── Settings (настройки)
└── Database: PostgreSQL (уже существует)
    ├── Data (ваши данные)
    └── Backups (резервные копии)
```

## Чек-лист перед деплоем

- [ ] Код загружен на GitHub
- [ ] Репозиторий подключен к Railway
- [ ] Переменная BOT_TOKEN добавлена
- [ ] Переменная DATABASE_URL добавлена
- [ ] Деплой завершен успешно (зеленая галочка)
- [ ] Логи показывают "Bot started"
- [ ] Бот отвечает на /start в Telegram
- [ ] Основные функции работают

## Полезные ссылки

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app
- Ваша БД: https://railway.app/project/[ваш-проект-id]
- GitHub Repo: https://github.com/[ваш-username]/telegram-warehouse-bot

## Поддержка

Если что-то не работает:
1. Проверьте логи в Railway
2. Проверьте переменные окружения
3. Проверьте, что БД доступна
4. Попробуйте перезапустить сервис

---

## 🎉 Готово!

После выполнения всех шагов ваш бот будет работать 24/7 на Railway.app!

**Преимущества:**
- ✅ Работает круглосуточно
- ✅ Автоматические обновления при git push
- ✅ Бесплатно (500 часов/месяц)
- ✅ Надежно и быстро
- ✅ Легко управлять

**Следующие шаги:**
1. Протестируйте все функции бота
2. Настройте уведомления
3. Включите автобэкапы БД
4. Мониторьте использование ресурсов

Удачи! 🚀
