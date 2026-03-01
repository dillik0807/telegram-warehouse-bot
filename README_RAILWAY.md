# 🤖 Telegram Warehouse Bot - Railway Deployment

## 📋 Что это?
Telegram бот для управления складом с веб-приложением. Работает 24/7 на Railway.app.

## ✅ Статус проекта
- **Код:** Готов к деплою
- **База данных:** PostgreSQL на Railway (уже настроена)
- **Конфигурация:** Все файлы на месте
- **Готовность:** 100%

## 🚀 Быстрый старт

### 1. Загрузите на GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/ВАШ-USERNAME/telegram-warehouse-bot.git
git push -u origin main
```

### 2. Деплой на Railway
1. https://railway.app → Login через GitHub
2. New Project → Deploy from GitHub repo
3. Выберите репозиторий
4. Добавьте переменные (см. ниже)

### 3. Переменные окружения
```
BOT_TOKEN=8333299455:AAGVaSEmB7AHyDqTb2bY3kwQ0hnbx8iCC2s
DATABASE_URL=postgresql://postgres:BsZJFBgvpSAiOYdLjBTusBKqHDMFdbVs@nozomi.proxy.rlwy.net:30779/railway
```

### 4. Готово!
Бот работает 24/7. Проверьте в Telegram: `/start`

## 📁 Структура проекта

```
telegram-warehouse-bot/
├── bot.py                          # Telegram бот (5600+ строк)
├── app.py                          # Flask веб-приложение
├── database.py                     # Функции работы с БД
├── config.py                       # Конфигурация
├── Procfile                        # Команда запуска для Railway
├── runtime.txt                     # Python 3.11.0
├── requirements.txt                # Зависимости
├── .env                           # Переменные (НЕ загружать на GitHub!)
├── .gitignore                     # Исключения для Git
└── templates/                     # HTML шаблоны (33 файла)
```

## 🎯 Функции бота

### Основные
- ✅ Авторизация (логин/пароль)
- ✅ Приходы товаров
- ✅ Расходы товаров
- ✅ Погашения долгов
- ✅ Партнеры
- ✅ Остатки на складах

### Отчеты
- ✅ Ежедневный отчет
- ✅ Месячный отчет
- ✅ Сводка по вагонам
- ✅ Карточка клиента
- ✅ Долги клиентов
- ✅ Экспорт в Excel

### Управление
- ✅ Клиенты
- ✅ Склады
- ✅ Фирмы
- ✅ Товары
- ✅ Цены
- ✅ Коалицы
- ✅ Пользователи (админы)

## 🌐 Веб-приложение

Доступно по адресу: (настроить отдельно на Railway)

### Страницы
- Приходы (с современным дизайном)
- Расходы
- Погашения
- Партнеры
- Отчеты
- Управление справочниками
- Долги клиентов

## 🔧 Технологии

### Backend
- Python 3.11
- python-telegram-bot 21.0
- Flask (веб-приложение)
- psycopg2 (PostgreSQL)

### Database
- PostgreSQL на Railway.app
- 10+ таблиц
- Автоматические бэкапы

### Hosting
- Railway.app (бот)
- Railway.app (БД)
- 500 часов бесплатно/месяц

## 📚 Документация

### Инструкции по деплою
- `QUICK_START_RAILWAY.md` - Быстрый старт (5 минут)
- `RAILWAY_DEPLOY_INSTRUCTIONS.md` - Подробная инструкция
- `DEPLOYMENT_CHECKLIST.md` - Чек-лист деплоя
- `RAILWAY_VARIABLES.txt` - Переменные окружения

### Отчеты
- `BOT_STATUS_REPORT.md` - Статус бота
- `PROJECT_STATUS_REPORT.md` - Статус проекта

### Руководства
- `DEPLOY_BOT_TO_RAILWAY.md` - Общее руководство по Railway

## 🔐 Безопасность

### Что НЕ загружать на GitHub
- ❌ `.env` файл (уже в .gitignore)
- ❌ Пароли и токены
- ❌ Данные пользователей

### Что загружать
- ✅ Код бота и приложения
- ✅ Конфигурационные файлы
- ✅ Документацию
- ✅ requirements.txt

## 💰 Стоимость

### Бесплатный план Railway
- ✅ 500 часов/месяц
- ✅ $5 кредитов/месяц
- ✅ Достаточно для 1 бота 24/7

### Если нужно больше
- Платный план: $5/месяц
- Unlimited часов
- Больше ресурсов

## 📊 Мониторинг

### Railway Dashboard
- Логи в реальном времени
- Использование ресурсов
- История деплоев
- Статус сервисов

### Уведомления
- Email при сбоях
- Webhook уведомления
- Telegram уведомления (настроить)

## 🔄 Обновление

### Автоматическое
```bash
git add .
git commit -m "Update"
git push
```
Railway автоматически обновит бота!

### Ручное
Railway → Settings → Restart

## 🆘 Поддержка

### Проблемы?
1. Проверьте логи: Railway → Deployments → View Logs
2. Проверьте переменные: Railway → Variables
3. Проверьте БД: Railway → Database

### Контакты
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Telegram Bot API: https://core.telegram.org/bots/api

## 📝 Changelog

### Version 2.0 (Текущая)
- ✅ Современный дизайн веб-приложения
- ✅ Форма добавления на главной странице
- ✅ Исправлена видимость текста на кнопках
- ✅ Добавлено редактирование всех записей
- ✅ Готов к деплою на Railway

### Version 1.0
- Базовая функциональность
- Telegram бот
- Веб-приложение
- База данных

## 🎯 Roadmap

### Планируется
- [ ] Мобильная версия веб-приложения
- [ ] Push-уведомления
- [ ] Интеграция с 1С
- [ ] API для внешних систем
- [ ] Аналитика и графики

## 👥 Команда

- **Разработчик:** Ваше имя
- **Дата создания:** 2024
- **Последнее обновление:** 01.03.2026

## 📄 Лицензия

Private project

---

## 🚀 Начать работу

1. Прочитайте `QUICK_START_RAILWAY.md`
2. Выполните команды из инструкции
3. Проверьте бота в Telegram
4. Готово! Бот работает 24/7

**Удачи!** 🎉
