# 🚀 Быстрый старт: Деплой бота на Railway

## Ваш проект готов! Выполните эти команды:

### 1️⃣ Инициализируйте Git
```bash
git init
git add .
git commit -m "Initial commit for Railway"
```

### 2️⃣ Создайте репозиторий на GitHub
1. Откройте: https://github.com/new
2. Название: `telegram-warehouse-bot`
3. Тип: **Private** (приватный)
4. Нажмите "Create repository"

### 3️⃣ Загрузите код на GitHub
Скопируйте команды с GitHub (они будут показаны после создания репозитория):
```bash
git remote add origin https://github.com/ВАШ-USERNAME/telegram-warehouse-bot.git
git branch -M main
git push -u origin main
```

### 4️⃣ Деплой на Railway
1. Откройте: https://railway.app
2. Войдите через GitHub
3. Нажмите "New Project"
4. Выберите "Deploy from GitHub repo"
5. Выберите `telegram-warehouse-bot`

### 5️⃣ Добавьте переменные окружения
В Railway → Variables → New Variable:

**Переменная 1:**
```
Name: BOT_TOKEN
Value: 8333299455:AAGVaSEmB7AHyDqTb2bY3kwQ0hnbx8iCC2s
```

**Переменная 2:**
```
Name: DATABASE_URL
Value: postgresql://postgres:BsZJFBgvpSAiOYdLjBTusBKqHDMFdbVs@nozomi.proxy.rlwy.net:30779/railway
```

### 6️⃣ Проверьте работу
1. Railway → Deployments → View Logs
2. Telegram → Найдите бота → `/start`

## ✅ Готово! Бот работает 24/7!

---

## 📝 Полная инструкция
Смотрите файл: `RAILWAY_DEPLOY_INSTRUCTIONS.md`

## ❓ Нужна помощь?
1. Проверьте логи в Railway
2. Убедитесь, что переменные добавлены правильно
3. Проверьте, что бот отвечает в Telegram
