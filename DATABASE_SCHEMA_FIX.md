# 🔧 Исправление схемы базы данных

## Проблема
При работе с разделами управления возникали ошибки из-за несоответствия названий полей в коде и реальной структуре таблиц базы данных.

## Ошибки

### 1. Таблица `prices`
**Ошибка**: `column p.created_by does not exist`

**Причина**: В коде использовались поля, которых нет в таблице.

**Реальная структура таблицы**:
```sql
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,              -- НЕ price_id
    product_name TEXT NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- НЕ created_at
    -- НЕТ поля created_by
)
```

### 2. Таблица `coalitions`
**Ошибка**: Использовалось неправильное имя поля при вставке и удалении.

**Реальная структура таблицы**:
```sql
CREATE TABLE coalitions (
    id SERIAL PRIMARY KEY,              -- НЕ coalition_id
    name TEXT NOT NULL,                 -- НЕ coalition_name
    contact TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## ✅ Исправления

### Файл: `app.py`

#### 1. Функция `manage_prices()` (строка ~695)
**Было**:
```python
cursor.execute("""
    SELECT p.price_id, p.product_name, p.price, p.created_at,
           u.username as created_by
    FROM prices p
    LEFT JOIN users u ON p.created_by = u.user_id
    ORDER BY p.created_at DESC
""")
```

**Стало**:
```python
cursor.execute("""
    SELECT id, product_name, price, updated_at
    FROM prices
    ORDER BY updated_at DESC
""")
```

#### 2. Функция `add_price_route()` (строка ~715)
**Было**:
```python
cursor.execute("""
    INSERT INTO prices (product_name, price, created_by, created_at)
    VALUES (%s, %s, %s, NOW())
""", (product_name, price, user_id))
```

**Стало**:
```python
cursor.execute("""
    INSERT INTO prices (product_name, price) 
    VALUES (%s, %s) 
    ON CONFLICT (product_name) 
    DO UPDATE SET price = %s, updated_at = CURRENT_TIMESTAMP
""", (product_name, price, price))
```

#### 3. Функция `delete_price_route()` (строка ~735)
**Было**:
```python
cursor.execute("DELETE FROM prices WHERE price_id = %s", (price_id,))
```

**Стало**:
```python
cursor.execute("DELETE FROM prices WHERE id = %s", (price_id,))
```

#### 4. Функция `add_coalition_route()` (строка ~755)
**Было**:
```python
cursor.execute("INSERT INTO coalitions (coalition_name) VALUES (%s)", (coalition_name,))
```

**Стало**:
```python
cursor.execute("INSERT INTO coalitions (name) VALUES (%s)", (coalition_name,))
```

#### 5. Функция `delete_coalition_route()` (строка ~770)
**Было**:
```python
cursor.execute("DELETE FROM coalitions WHERE coalition_id = %s", (coalition_id,))
```

**Стало**:
```python
cursor.execute("DELETE FROM coalitions WHERE id = %s", (coalition_id,))
```

### Файл: `templates/manage_prices.html`

**Изменения**:
- Убрана колонка "Установил" (так как нет поля `created_by`)
- Изменено "Дата установки" на "Дата обновления"
- Исправлены индексы полей в цикле (price[0], price[1], price[2], price[3])
- Изменен colspan с 6 на 5

## 📊 Сводка изменений

| Таблица | Поле в коде (было) | Поле в БД (стало) |
|---------|-------------------|-------------------|
| prices | price_id | id |
| prices | created_at | updated_at |
| prices | created_by | (удалено) |
| coalitions | coalition_name | name |
| coalitions | coalition_id | id |

## 🎯 Функциональность

### Управление ценами
- ✅ Просмотр списка цен
- ✅ Установка/обновление цены (с ON CONFLICT)
- ✅ Удаление цены
- ✅ Отображение даты последнего обновления

### Управление коалицей
- ✅ Просмотр списка коалиц
- ✅ Добавление новой коалицы
- ✅ Удаление коалицы (с проверкой использования)

## 🔍 Проверка

После исправлений все разделы управления работают корректно:
- 📦 Товары - работает
- 🏭 Фирмы - работает
- 💰 Цены - работает (исправлено)
- 📊 Коалица - работает (исправлено)

## 📝 Примечания

1. **Цены**: Используется `ON CONFLICT` для обновления существующей цены вместо создания дубликата
2. **Коалиция**: Проверка использования перед удалением защищает от удаления используемых записей
3. **Автоматическое обновление**: Поле `updated_at` обновляется автоматически при изменении цены

---

**Статус**: ✅ Исправлено
**Дата**: 2026-02-25
**Версия**: 2.2 (Исправлена схема БД)
