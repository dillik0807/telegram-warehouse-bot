# ✅ Чек-лист деплоя на Railway.app

## Подготовка (на вашем компьютере)

### Шаг 1: Проверка файлов
- [x] `bot.py` - код бота
- [x] `database.py` - функции БД
- [x] `config.py` - конфигурация
- [x] `Procfile` - команда запуска
- [x] `runtime.txt` - версия Python
- [x] `requirements.txt` - зависимости
- [x] `.gitignore` - исключения для Git
- [x] `.env` - переменные (НЕ загружать на GitHub!)

### Шаг 2: Git инициализация
```bash
git init
git add .
git commit -m "Initial commit for Railway"
```
- [ ] Git инициализирован
- [ ] Файлы добавлены в commit

### Шаг 3: GitHub репозиторий
1. Создайте репозиторий: https://github.com/new
   - [ ] Название: `telegram-warehouse-bot`
   - [ ] Тип: Private
   - [ ] Создан

2. Загрузите код:
```bash
git remote add origin https://github.com/ВАШ-USERNAME/telegram-warehouse-bot.git
git branch -M main
git push -u origin main
```
- [ ] Код загружен на GitHub
- [ ] Репозиторий виден на GitHub

## Деплой на Railway

### Шаг 4: Создание проекта
1. Откройте: https://railway.app
   - [ ] Вошли через GitHub
   
2. Создайте проект:
   - [ ] Нажали "New Project"
   - [ ] Выбрали "Deploy from GitHub repo"
   - [ ] Выбрали репозиторий `telegram-warehouse-bot`
   - [ ] Деплой начался

### Шаг 5: Переменные окружения
В Railway → Variables → New Variable:

**BOT_TOKEN:**
```
8333299455:AAGVaSEmB7AHyDqTb2bY3kwQ0hnbx8iCC2s
```
- [ ] Переменная BOT_TOKEN добавлена

**DATABASE_URL:**
```
postgresql://postgres:BsZJFBgvpSAiOYdLjBTusBKqHDMFdbVs@nozomi.proxy.rlwy.net:30779/railway
```
- [ ] Переменная DATABASE_URL добавлена

### Шаг 6: Проверка деплоя
Railway → Deployments:
- [ ] Статус: Success (зеленая галочка)
- [ ] Время деплоя: ~2-3 минуты
- [ ] Нет ошибок в логах

### Шаг 7: Проверка логов
Railway → Deployments → View Logs:
- [ ] Логи показывают "Bot started" или подобное
- [ ] Нет ошибок подключения к БД
- [ ] Нет ошибок импорта модулей

## Тестирование бота

### Шаг 8: Проверка в Telegram
1. Откройте Telegram
   - [ ] Нашли бота
   
2. Отправьте команды:
   - [ ] `/start` - бот отвечает
   - [ ] Главное меню отображается
   - [ ] Кнопки работают

### Шаг 9: Проверка функций
- [ ] Авторизация работает
- [ ] Добавление прихода работает
- [ ] Просмотр остатков работает
- [ ] Добавление расхода работает
- [ ] Отчеты работают

## Настройка мониторинга

### Шаг 10: Уведомления
Railway → Project Settings → Notifications:
- [ ] Email уведомления включены
- [ ] Уведомления о сбоях включены

### Шаг 11: Резервное копирование
Railway → Database → Settings:
- [ ] Automated Backups включены
- [ ] Частота: Daily (ежедневно)

## Финальная проверка

### Шаг 12: Проверка ресурсов
Railway → Project Settings → Usage:
- [ ] Execution Time: показывает часы работы
- [ ] Credits Used: в пределах бесплатного плана
- [ ] Нет предупреждений

### Шаг 13: Документация
- [ ] Сохранили ссылку на Railway проект
- [ ] Сохранили ссылку на GitHub репозиторий
- [ ] Записали данные для доступа

## 🎉 Деплой завершен!

Если все пункты отмечены ✅ - ваш бот работает 24/7 на Railway!

## Что дальше?

### Обновление бота
Когда изменили код:
```bash
git add .
git commit -m "Update bot"
git push
```
Railway автоматически обновит бота!

### Просмотр логов
Railway → Deployments → View Logs

### Перезапуск
Railway → Settings → Restart

### Остановка
Railway → Settings → Remove Service

## Полезные ссылки

- Railway Dashboard: https://railway.app/dashboard
- GitHub Repo: https://github.com/ВАШ-USERNAME/telegram-warehouse-bot
- Telegram Bot: @ваш_бот_username

## Контакты поддержки

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Telegram Bot API: https://core.telegram.org/bots/api

---

**Дата деплоя:** _________________
**Статус:** ✅ Работает / ❌ Требует исправлений
**Примечания:** _________________
