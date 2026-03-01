# Веб-приложение системы учета

## Описание
Веб-приложение для удаленного доступа к системе учета товаров. Имеет тот же функционал, что и Telegram бот.

## Возможности

### Для всех пользователей:
- ➕ Добавление приходов товаров
- ➖ Добавление расходов товаров
- 💰 Учет погашений
- 🤝 Учет партнеров
- 📊 Просмотр отчетов:
  - 💳 Долги клиентов
  - 📅 Отчет за день (приходы и расходы)
  - 📤 Расход за день (по складам и товарам)
  - 🏭 Фактический остаток (по коалициям и складам)
  - ➕ Отчет по приходам (группировка по месяцам)
  - ➖ Отчет по расходам (группировка по месяцам)
  - 💰 Отчет по погашениям (детальный список)
  - 🤝 Отчет по партнерам (детальный список)
  - 👤 Карточка клиента (покупки, погашения, баланс)
  - 📢 Уведомления о долгах (по датам)
  - 🚂 Итоги вагонов (сводка по складам)
  - 📥 Список приходов (детальный)
  - 📤 Список расходов (детальный)

### Для администраторов:
- 👥 Управление пользователями
- 🏢 Управление складами
- 👤 Управление клиентами
- 🏭 Управление фирмами
- 📊 Управление коалициями

## Установка

1. Установите зависимости:
```bash
pip install -r requirements_web.txt
```

2. Убедитесь, что база данных настроена (используется та же БД, что и для бота)

3. Запустите приложение:
```bash
python app.py
```

4. Откройте браузер и перейдите по адресу:
```
http://localhost:5000
```

## Вход в систему

Используйте те же логин и пароль, что и для Telegram бота.

Если у вас еще нет учетной записи, администратор должен создать ее через бота или напрямую в базе данных.

## Развертывание на сервере

### Вариант 1: Heroku

1. Создайте файл `Procfile`:
```
web: gunicorn app:app
```

2. Добавьте gunicorn в requirements_web.txt:
```
gunicorn==20.1.0
```

3. Разверните на Heroku:
```bash
heroku create your-app-name
git push heroku main
```

### Вариант 2: VPS (Ubuntu)

1. Установите необходимые пакеты:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

2. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_web.txt
pip install gunicorn
```

3. Создайте systemd service:
```bash
sudo nano /etc/systemd/system/inventory-app.service
```

Содержимое:
```ini
[Unit]
Description=Inventory Web App
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/app/venv/bin"
ExecStart=/path/to/your/app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

4. Запустите сервис:
```bash
sudo systemctl start inventory-app
sudo systemctl enable inventory-app
```

5. Настройте Nginx:
```bash
sudo nano /etc/nginx/sites-available/inventory-app
```

Содержимое:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. Активируйте конфигурацию:
```bash
sudo ln -s /etc/nginx/sites-available/inventory-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Безопасность

⚠️ **ВАЖНО:** Перед развертыванием в продакшене:

1. Измените `app.secret_key` в app.py на случайную строку
2. Установите `debug=False` в app.run()
3. Используйте HTTPS (Let's Encrypt)
4. Настройте firewall
5. Регулярно обновляйте зависимости

## Структура проекта

```
.
├── app.py                  # Главный файл приложения
├── database.py             # Функции работы с БД (общие с ботом)
├── config.py               # Конфигурация
├── templates/              # HTML шаблоны
│   ├── base.html          # Базовый шаблон
│   ├── login.html         # Страница входа
│   ├── index.html         # Главная страница
│   ├── arrivals.html      # Список приходов
│   ├── departures.html    # Список расходов
│   └── ...
└── static/                 # Статические файлы (CSS, JS, изображения)
```

## Поддержка

Для вопросов и поддержки обращайтесь к администратору системы.
