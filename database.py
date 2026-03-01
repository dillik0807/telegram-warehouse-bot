import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from config import DATABASE_URL

def get_connection():
    """Получить подключение к базе данных"""
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Инициализация базы данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            quantity INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            type TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            user_id BIGINT PRIMARY KEY,
            username TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS warehouse_groups (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS warehouses (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT,
            group_id INTEGER REFERENCES warehouse_groups(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS firms (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            contact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            product_name TEXT NOT NULL UNIQUE,
            price DECIMAL(10, 2) NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coalitions (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            contact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username TEXT,
            role TEXT DEFAULT 'manager',
            warehouse_group_id INTEGER REFERENCES warehouse_groups(id),
            is_active BOOLEAN DEFAULT TRUE,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_logs (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            action TEXT NOT NULL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

def add_product(name, quantity):
    """Добавить приход товара"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Используем SELECT FOR UPDATE для блокировки строки
        cursor.execute('SELECT quantity FROM products WHERE name = %s FOR UPDATE', (name,))
        result = cursor.fetchone()
        
        if result:
            new_quantity = result[0] + quantity
            cursor.execute('UPDATE products SET quantity = %s WHERE name = %s', (new_quantity, name))
        else:
            cursor.execute('INSERT INTO products (name, quantity) VALUES (%s, %s)', (name, quantity))
        
        cursor.execute('INSERT INTO transactions (product_name, quantity, type) VALUES (%s, %s, %s)',
                       (name, quantity, 'приход'))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False

def remove_product(name, quantity):
    """Вывод товара"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Используем SELECT FOR UPDATE для блокировки строки
        cursor.execute('SELECT quantity FROM products WHERE name = %s FOR UPDATE', (name,))
        result = cursor.fetchone()
        
        if not result:
            cursor.close()
            conn.close()
            return False, "Товар не найден"
        
        current_quantity = result[0]
        if current_quantity < quantity:
            cursor.close()
            conn.close()
            return False, f"Недостаточно товара. Доступно: {current_quantity}"
        
        new_quantity = current_quantity - quantity
        cursor.execute('UPDATE products SET quantity = %s WHERE name = %s', (new_quantity, name))
        cursor.execute('INSERT INTO transactions (product_name, quantity, type) VALUES (%s, %s, %s)',
                       (name, quantity, 'вывод'))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Успешно"
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)

def get_inventory():
    """Получить список всех товаров"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, quantity FROM products ORDER BY name')
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_history(limit=10):
    """Получить историю операций"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT product_name, quantity, type, date 
        FROM transactions 
        ORDER BY date DESC 
        LIMIT %s
    ''', (limit,))
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history


def add_admin(user_id, username):
    """Добавить администратора"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO admins (user_id, username) VALUES (%s, %s) ON CONFLICT (user_id) DO NOTHING',
                   (user_id, username))
    conn.commit()
    cursor.close()
    conn.close()

def remove_admin(user_id):
    """Удалить администратора"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM admins WHERE user_id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_admins():
    """Получить список администраторов"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, username, added_at FROM admins ORDER BY added_at')
    admins = cursor.fetchall()
    cursor.close()
    conn.close()
    return admins

def is_admin(user_id):
    """Проверить, является ли пользователь администратором"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM admins WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def get_report():
    """Получить отчет по товарам"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Общая статистика
    cursor.execute('SELECT COUNT(*), COALESCE(SUM(quantity), 0) FROM products')
    total_products, total_quantity = cursor.fetchone()
    
    # Статистика операций
    cursor.execute('SELECT COUNT(*) FROM transactions WHERE type = %s', ('приход',))
    total_income = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM transactions WHERE type = %s', ('вывод',))
    total_outcome = cursor.fetchone()[0]
    
    # Топ товаров
    cursor.execute('SELECT name, quantity FROM products ORDER BY quantity DESC LIMIT 5')
    top_products = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {
        'total_products': total_products,
        'total_quantity': total_quantity,
        'total_income': total_income,
        'total_outcome': total_outcome,
        'top_products': top_products
    }


def add_warehouse(name, address, group_id=None):
    """Добавить склад"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO warehouses (name, address, group_id) VALUES (%s, %s, %s)', 
                   (name, address, group_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_warehouses():
    """Получить список складов"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT w.id, w.name, w.address, wg.name as group_name
        FROM warehouses w
        LEFT JOIN warehouse_groups wg ON w.group_id = wg.id
        ORDER BY wg.name, w.name
    ''')
    warehouses = cursor.fetchall()
    cursor.close()
    conn.close()
    return warehouses

def get_warehouse_by_id(warehouse_id):
    """Получить название склада по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM warehouses WHERE id = %s', (warehouse_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def add_warehouse_group(name):
    """Добавить подгруппу складов"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO warehouse_groups (name) VALUES (%s)', (name,))
    conn.commit()
    cursor.close()
    conn.close()

def get_warehouse_groups():
    """Получить список подгрупп складов"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM warehouse_groups ORDER BY name')
    groups = cursor.fetchall()
    cursor.close()
    conn.close()
    return groups

def add_firm(name, contact):
    """Добавить фирму"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO firms (name, contact) VALUES (%s, %s)', (name, contact))
    conn.commit()
    cursor.close()
    conn.close()

def get_firms():
    """Получить список фирм"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, contact FROM firms ORDER BY name')
    firms = cursor.fetchall()
    cursor.close()
    conn.close()
    return firms

def get_firm_by_id(firm_id):
    """Получить название фирмы по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM firms WHERE id = %s', (firm_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def add_client(name, phone):
    """Добавить клиента"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (name, phone) VALUES (%s, %s)', (name, phone))
    conn.commit()
    cursor.close()
    conn.close()

def get_clients():
    """Получить список клиентов"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, phone FROM clients ORDER BY name')
    clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return clients

def get_client_by_id(client_id):
    """Получить название клиента по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM clients WHERE id = %s', (client_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def set_product_price(product_name, price):
    """Установить цену товара"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO prices (product_name, price) 
        VALUES (%s, %s) 
        ON CONFLICT (product_name) 
        DO UPDATE SET price = %s, updated_at = CURRENT_TIMESTAMP
    ''', (product_name, price, price))
    conn.commit()
    cursor.close()
    conn.close()

def get_product_prices():
    """Получить список цен на товары"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT product_name, price FROM prices ORDER BY product_name')
    raw_prices = cursor.fetchall()
    cursor.close()
    conn.close()
    # Конвертируем Decimal в float для корректного отображения
    prices = [(name, float(price)) for name, price in raw_prices]
    return prices

def get_product_price(product_name):
    """Получить цену конкретного товара"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT price FROM prices WHERE product_name = %s', (product_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return float(result[0])
    return None


def delete_warehouse(warehouse_id):
    """Удалить склад"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM warehouses WHERE id = %s', (warehouse_id,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_warehouse_group(group_id):
    """Удалить подгруппу складов"""
    conn = get_connection()
    cursor = conn.cursor()
    # Сначала обнуляем ссылки на подгруппу в складах
    cursor.execute('UPDATE warehouses SET group_id = NULL WHERE group_id = %s', (group_id,))
    cursor.execute('DELETE FROM warehouse_groups WHERE id = %s', (group_id,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_product(product_name):
    """Удалить товар"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE name = %s', (product_name,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_firm(firm_id):
    """Удалить фирму"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM firms WHERE id = %s', (firm_id,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_client(client_id):
    """Удалить клиента"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clients WHERE id = %s', (client_id,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_price(product_name):
    """Удалить цену товара"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM prices WHERE product_name = %s', (product_name,))
    conn.commit()
    cursor.close()
    conn.close()


def set_product_quantity(product_name, quantity):
    """Установить количество товара"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET quantity = %s WHERE name = %s', (quantity, product_name))
    conn.commit()
    cursor.close()
    conn.close()


def undo_last_transaction():
    """Отменить последнюю транзакцию"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Получаем последнюю транзакцию
        cursor.execute('''
            SELECT id, product_name, quantity, type, date 
            FROM transactions 
            ORDER BY date DESC 
            LIMIT 1
        ''')
        transaction = cursor.fetchone()
        
        if not transaction:
            cursor.close()
            conn.close()
            return {'success': False, 'message': 'Нет транзакций для отмены'}
        
        trans_id, product_name, quantity, trans_type, date = transaction
        
        # Получаем текущее количество товара
        cursor.execute('SELECT quantity FROM products WHERE name = %s', (product_name,))
        result = cursor.fetchone()
        
        if not result:
            cursor.close()
            conn.close()
            return {'success': False, 'message': f'Товар "{product_name}" не найден'}
        
        current_quantity = result[0]
        
        # Отменяем операцию (делаем обратное действие)
        if trans_type == 'приход':
            # Если был приход, то вычитаем
            new_quantity = current_quantity - quantity
            if new_quantity < 0:
                cursor.close()
                conn.close()
                return {'success': False, 'message': f'Невозможно отменить: недостаточно товара (текущее: {current_quantity}, нужно вычесть: {quantity})'}
        else:
            # Если был вывод, то добавляем
            new_quantity = current_quantity + quantity
        
        # Обновляем количество
        cursor.execute('UPDATE products SET quantity = %s WHERE name = %s', (new_quantity, product_name))
        
        # Удаляем транзакцию
        cursor.execute('DELETE FROM transactions WHERE id = %s', (trans_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'product_name': product_name,
            'quantity': quantity,
            'type': trans_type,
            'date': str(date)
        }
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return {'success': False, 'message': f'Ошибка: {str(e)}'}


def add_coalition(name, contact):
    """Добавить коалицу"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO coalitions (name, contact) VALUES (%s, %s)', (name, contact))
    conn.commit()
    cursor.close()
    conn.close()

def get_coalitions():
    """Получить список коалиц"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, contact FROM coalitions ORDER BY name')
    coalitions = cursor.fetchall()
    cursor.close()
    conn.close()
    return coalitions

def get_coalition_by_id(coalition_id):
    """Получить название коалиции по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM coalitions WHERE id = %s', (coalition_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def delete_coalition(coalition_id):
    """Удалить коалицу"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM coalitions WHERE id = %s', (coalition_id,))
    conn.commit()
    cursor.close()
    conn.close()


# ============= СИСТЕМА РОЛЕЙ =============

def add_user(user_id, username, role='manager', warehouse_group_id=None):
    """Добавить пользователя с ролью"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, username, role, warehouse_group_id) 
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id) 
        DO UPDATE SET username = %s, role = %s, warehouse_group_id = %s
    ''', (user_id, username, role, warehouse_group_id, username, role, warehouse_group_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_user_role(user_id):
    """Получить роль пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role, warehouse_group_id, is_active FROM users WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result if result else (None, None, False)

def get_all_users():
    """Получить список всех пользователей"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.user_id, u.username, u.role, wg.name as group_name, u.is_active, u.added_at
        FROM users u
        LEFT JOIN warehouse_groups wg ON u.warehouse_group_id = wg.id
        ORDER BY u.added_at DESC
    ''')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def update_user_role(user_id, role):
    """Обновить роль пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET role = %s WHERE user_id = %s', (role, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_user_warehouse_group(user_id, warehouse_group_id):
    """Обновить группу складов пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET warehouse_group_id = %s WHERE user_id = %s', 
                   (warehouse_group_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def deactivate_user(user_id):
    """Деактивировать пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_active = FALSE WHERE user_id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def activate_user(user_id):
    """Активировать пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_active = TRUE WHERE user_id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_user(user_id):
    """Удалить пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def log_access(user_id, action, details=""):
    """Записать лог доступа"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO access_logs (user_id, action, details) VALUES (%s, %s, %s)',
                   (user_id, action, details))
    conn.commit()
    cursor.close()
    conn.close()

def has_permission(user_id, required_role):
    """Проверить права доступа пользователя"""
    role_hierarchy = {
        'admin': 4,
        'warehouse_manager': 3,
        'manager': 2,
        'cashier': 1
    }
    
    role, warehouse_group_id, is_active = get_user_role(user_id)
    
    if not is_active:
        return False
    
    if role not in role_hierarchy or required_role not in role_hierarchy:
        return False
    
    return role_hierarchy[role] >= role_hierarchy[required_role]

def get_user_warehouses(user_id):
    """Получить склады доступные пользователю"""
    role, warehouse_group_id, is_active = get_user_role(user_id)
    
    if not is_active:
        return []
    
    # Админ видит все склады
    if role == 'admin':
        return get_warehouses()
    
    # Остальные видят только склады своей группы
    if warehouse_group_id:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT w.id, w.name, w.address, wg.name as group_name
            FROM warehouses w
            LEFT JOIN warehouse_groups wg ON w.group_id = wg.id
            WHERE w.group_id = %s
            ORDER BY w.name
        ''', (warehouse_group_id,))
        warehouses = cursor.fetchall()
        cursor.close()
        conn.close()
        return warehouses
    
    return []


# ============= СИСТЕМА ЛОГИН/ПАРОЛЬ =============

def add_user_with_login(login, password, username, role='manager', warehouse_group_id=None):
    """Добавить пользователя с логином и паролем"""
    import hashlib
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Хешируем пароль
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Генерируем уникальный user_id
    cursor.execute('SELECT MAX(user_id) FROM users')
    max_id = cursor.fetchone()[0]
    new_user_id = (max_id + 1) if max_id else 1000000
    
    try:
        cursor.execute('''
            INSERT INTO users (user_id, login, password, username, role, warehouse_group_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (new_user_id, login, password_hash, username, role, warehouse_group_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, new_user_id
    except psycopg2.IntegrityError:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, "Логин уже существует"

def verify_login(login, password):
    """Проверить логин и пароль"""
    import hashlib
    
    conn = get_connection()
    cursor = conn.cursor()
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
        SELECT user_id, username, role, warehouse_group_id, is_active 
        FROM users 
        WHERE login = %s AND password = %s
    ''', (login, password_hash))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        user_id, username, role, warehouse_group_id, is_active = result
        if is_active:
            return True, user_id, username, role, warehouse_group_id
        else:
            return False, None, None, None, None
    return False, None, None, None, None

def create_session(telegram_id, user_id):
    """Создать сессию для пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_sessions (telegram_id, user_id) 
        VALUES (%s, %s)
        ON CONFLICT (telegram_id) 
        DO UPDATE SET user_id = %s, last_activity = CURRENT_TIMESTAMP
    ''', (telegram_id, user_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_session(telegram_id):
    """Получить сессию пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT us.user_id, u.username, u.role, u.warehouse_group_id, u.is_active
        FROM user_sessions us
        JOIN users u ON us.user_id = u.user_id
        WHERE us.telegram_id = %s
    ''', (telegram_id,))
    result = cursor.fetchone()
    
    # Обновляем время последней активности
    if result:
        cursor.execute('''
            UPDATE user_sessions 
            SET last_activity = CURRENT_TIMESTAMP 
            WHERE telegram_id = %s
        ''', (telegram_id,))
        conn.commit()
    
    cursor.close()
    conn.close()
    return result

def logout_session(telegram_id):
    """Выйти из сессии"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_sessions WHERE telegram_id = %s', (telegram_id,))
    conn.commit()
    cursor.close()
    conn.close()

def change_password(user_id, new_password):
    """Изменить пароль пользователя"""
    import hashlib
    
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    cursor.execute('UPDATE users SET password = %s WHERE user_id = %s', (password_hash, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_id(user_id):
    """Получить информацию о пользователе по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id, login, username, role, warehouse_group_id, is_active
        FROM users 
        WHERE user_id = %s
    ''', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


# ============= ДЕТАЛЬНЫЙ УЧЕТ ПРИХОДА =============

def add_arrival(arrival_date, wagon_number, firm_id, warehouse_id, product_name, 
                source, quantity_document, quantity_actual, notes, created_by):
    """Добавить детальный приход товара"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Добавляем запись о приходе
        cursor.execute('''
            INSERT INTO arrivals 
            (arrival_date, wagon_number, firm_id, warehouse_id, product_name, 
             source, quantity_document, quantity_actual, notes, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (arrival_date, wagon_number, firm_id, warehouse_id, product_name,
              source, quantity_document, quantity_actual, notes, created_by))
        
        arrival_id = cursor.fetchone()[0]
        
        # Добавляем в историю транзакций
        cursor.execute('''
            INSERT INTO transactions (product_name, quantity, type) 
            VALUES (%s, %s, %s)
        ''', (product_name, quantity_actual, 'приход'))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, arrival_id
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)

def get_arrivals(limit=50, warehouse_id=None, firm_id=None, date_from=None, date_to=None):
    """Получить список приходов с фильтрами"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT a.id, a.arrival_date, a.wagon_number, f.name as firm_name, 
               w.name as warehouse_name, a.product_name, a.source,
               a.quantity_document, a.quantity_actual, a.notes, 
               u.username, a.created_at
        FROM arrivals a
        LEFT JOIN firms f ON a.firm_id = f.id
        LEFT JOIN warehouses w ON a.warehouse_id = w.id
        LEFT JOIN users u ON a.created_by = u.user_id
        WHERE 1=1
    '''
    params = []
    
    if warehouse_id:
        query += ' AND a.warehouse_id = %s'
        params.append(warehouse_id)
    
    if firm_id:
        query += ' AND a.firm_id = %s'
        params.append(firm_id)
    
    if date_from:
        query += ' AND a.arrival_date >= %s'
        params.append(date_from)
    
    if date_to:
        query += ' AND a.arrival_date <= %s'
        params.append(date_to)
    
    query += ' ORDER BY a.arrival_date DESC, a.created_at DESC LIMIT %s'
    params.append(limit)
    
    cursor.execute(query, params)
    arrivals = cursor.fetchall()
    cursor.close()
    conn.close()
    return arrivals

def get_arrival_by_id(arrival_id):
    """Получить детальную информацию о приходе"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.id, a.arrival_date, a.wagon_number, f.name as firm_name, 
               w.name as warehouse_name, a.product_name, a.source,
               a.quantity_document, a.quantity_actual, a.notes, 
               u.username, a.created_at
        FROM arrivals a
        LEFT JOIN firms f ON a.firm_id = f.id
        LEFT JOIN warehouses w ON a.warehouse_id = w.id
        LEFT JOIN users u ON a.created_by = u.user_id
        WHERE a.id = %s
    ''', (arrival_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_arrival_statistics(date_from=None, date_to=None):
    """Получить статистику по приходам"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            COUNT(*) as total_arrivals,
            SUM(quantity_actual) as total_quantity,
            SUM(quantity_document - quantity_actual) as total_difference
        FROM arrivals
        WHERE 1=1
    '''
    params = []
    
    if date_from:
        query += ' AND arrival_date >= %s'
        params.append(date_from)
    
    if date_to:
        query += ' AND arrival_date <= %s'
        params.append(date_to)
    
    cursor.execute(query, params)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def get_inventory_by_warehouse_group(warehouse_group_id):
    """Получить остатки товаров по группе складов"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Получаем приходы и выводы на склады этой группы
    cursor.execute('''
        SELECT 
            product_name,
            COALESCE(SUM(arrivals), 0) - COALESCE(SUM(departures), 0) as total_quantity
        FROM (
            SELECT a.product_name, a.quantity_actual as arrivals, 0 as departures
            FROM arrivals a
            JOIN warehouses w ON a.warehouse_id = w.id
            WHERE w.group_id = %s
            
            UNION ALL
            
            SELECT d.product_name, 0 as arrivals, d.quantity as departures
            FROM departures d
            JOIN warehouses w ON d.warehouse_id = w.id
            WHERE w.group_id = %s
        ) combined
        GROUP BY product_name
        HAVING COALESCE(SUM(arrivals), 0) - COALESCE(SUM(departures), 0) > 0
        ORDER BY product_name
    ''', (warehouse_group_id, warehouse_group_id))
    
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_inventory_detailed():
    """Получить детальные остатки товаров (приход, расход, остаток)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            product_name,
            COALESCE(SUM(arrivals), 0) as total_arrivals,
            COALESCE(SUM(departures), 0) as total_departures,
            COALESCE(SUM(arrivals), 0) - COALESCE(SUM(departures), 0) as balance
        FROM (
            SELECT a.product_name, a.quantity_actual as arrivals, 0 as departures
            FROM arrivals a
            
            UNION ALL
            
            SELECT d.product_name, 0 as arrivals, d.quantity as departures
            FROM departures d
        ) combined
        GROUP BY product_name
        HAVING COALESCE(SUM(arrivals), 0) - COALESCE(SUM(departures), 0) > 0
        ORDER BY product_name
    ''')
    
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_inventory_detailed_by_warehouse_group(warehouse_group_id):
    """Получить детальные остатки товаров по группе складов (приход, расход, остаток)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            product_name,
            COALESCE(SUM(arrivals), 0) as total_arrivals,
            COALESCE(SUM(departures), 0) as total_departures,
            COALESCE(SUM(arrivals), 0) - COALESCE(SUM(departures), 0) as balance
        FROM (
            SELECT a.product_name, a.quantity_actual as arrivals, 0 as departures
            FROM arrivals a
            JOIN warehouses w ON a.warehouse_id = w.id
            WHERE w.group_id = %s
            
            UNION ALL
            
            SELECT d.product_name, 0 as arrivals, d.quantity as departures
            FROM departures d
            JOIN warehouses w ON d.warehouse_id = w.id
            WHERE w.group_id = %s
        ) combined
        GROUP BY product_name
        HAVING COALESCE(SUM(arrivals), 0) - COALESCE(SUM(departures), 0) > 0
        ORDER BY product_name
    ''', (warehouse_group_id, warehouse_group_id))
    
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_inventory_by_user(user_id):
    """Получить остатки товаров доступные пользователю"""
    role, warehouse_group_id, is_active = get_user_role(user_id)
    
    if not is_active:
        return []
    
    # Админ видит все остатки
    if role == 'admin':
        return get_inventory()
    
    # Остальные видят только остатки своей группы складов
    if warehouse_group_id:
        return get_inventory_by_warehouse_group(warehouse_group_id)
    
    return []

def get_inventory_detailed_by_user(user_id):
    """Получить детальные остатки товаров доступные пользователю (приход, расход, остаток)"""
    role, warehouse_group_id, is_active = get_user_role(user_id)
    
    if not is_active:
        return []
    
    # Админ видит все остатки
    if role == 'admin':
        return get_inventory_detailed()
    
    # Остальные видят только остатки своей группы складов
    if warehouse_group_id:
        return get_inventory_detailed_by_warehouse_group(warehouse_group_id)
    
    return []


# ============= ДЕТАЛЬНЫЙ УЧЕТ ВЫВОДА =============

def add_departure(departure_date, coalition_id, firm_id, warehouse_id, product_name,
                  quantity, price, notes, created_by, client_id=None):
    """Добавить детальный вывод товара"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Проверяем реальный остаток товара на основе приходов и расходов
        cursor.execute('''
            SELECT COALESCE(SUM(arrivals), 0) - COALESCE(SUM(departures), 0) as balance
            FROM (
                SELECT SUM(quantity_actual) as arrivals, 0 as departures
                FROM arrivals
                WHERE product_name = %s
                
                UNION ALL
                
                SELECT 0 as arrivals, SUM(quantity) as departures
                FROM departures
                WHERE product_name = %s
            ) combined
        ''', (product_name, product_name))
        
        result = cursor.fetchone()
        current_quantity = result[0] if result else 0
        
        if current_quantity <= 0:
            cursor.close()
            conn.close()
            return False, "Товар не найден или остаток равен нулю"
        
        if current_quantity < quantity:
            cursor.close()
            conn.close()
            return False, f"Недостаточно товара. Доступно: {current_quantity}"
        
        # Рассчитываем total по формуле: (quantity / 20) * price
        total = (quantity / 20) * price
        
        # Добавляем запись о выводе
        cursor.execute('''
            INSERT INTO departures 
            (departure_date, coalition_id, firm_id, warehouse_id, product_name,
             quantity, price, total, notes, created_by, client_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (departure_date, coalition_id, firm_id, warehouse_id, product_name,
              quantity, price, total, notes, created_by, client_id))
        
        departure_id = cursor.fetchone()[0]
        
        # Добавляем в историю транзакций
        cursor.execute('''
            INSERT INTO transactions (product_name, quantity, type)
            VALUES (%s, %s, %s)
        ''', (product_name, quantity, 'вывод'))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, departure_id
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)

def get_departures(limit=50, warehouse_id=None, coalition_id=None, date_from=None, date_to=None, departure_id=None):
    """Получить список выводов с фильтрами"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT d.id, d.departure_date, c.name as coalition_name, f.name as firm_name,
               w.name as warehouse_name, d.product_name, d.quantity, d.price,
               d.notes, u.username, d.created_at, cl.name as client_name, d.total
        FROM departures d
        LEFT JOIN coalitions c ON d.coalition_id = c.id
        LEFT JOIN firms f ON d.firm_id = f.id
        LEFT JOIN warehouses w ON d.warehouse_id = w.id
        LEFT JOIN users u ON d.created_by = u.user_id
        LEFT JOIN clients cl ON d.client_id = cl.id
        WHERE 1=1
    '''
    params = []
    
    if departure_id:
        query += ' AND d.id = %s'
        params.append(departure_id)
    
    if warehouse_id:
        query += ' AND d.warehouse_id = %s'
        params.append(warehouse_id)
    
    if coalition_id:
        query += ' AND d.coalition_id = %s'
        params.append(coalition_id)
    
    if date_from:
        query += ' AND d.departure_date >= %s'
        params.append(date_from)
    
    if date_to:
        query += ' AND d.departure_date <= %s'
        params.append(date_to)
    
    query += ' ORDER BY d.departure_date DESC, d.created_at DESC LIMIT %s'
    params.append(limit)
    
    cursor.execute(query, params)
    departures = cursor.fetchall()
    cursor.close()
    conn.close()
    return departures


# ============= ПОГАШЕНИЯ =============

def add_payment(payment_date, client_id, somoni, dollar, exchange_rate, notes, created_by):
    """Добавить погашение"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Вычисляем общую сумму в долларах: сомони / курс
        total_usd = somoni / exchange_rate
        
        cursor.execute('''
            INSERT INTO payments 
            (payment_date, client_id, somoni, dollar, exchange_rate, total_usd, notes, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (payment_date, client_id, somoni, 0, exchange_rate, total_usd, notes, created_by))
        
        payment_id = cursor.fetchone()[0]
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, payment_id
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)

def get_payments(limit=50, client_id=None, date_from=None, date_to=None):
    """Получить список погашений с фильтрами"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT p.id, p.payment_date, cl.name as client_name, p.somoni, p.dollar,
               p.exchange_rate, p.total_usd, p.notes, u.username, p.created_at
        FROM payments p
        LEFT JOIN clients cl ON p.client_id = cl.id
        LEFT JOIN users u ON p.created_by = u.user_id
        WHERE 1=1
    '''
    params = []
    
    if client_id:
        query += ' AND p.client_id = %s'
        params.append(client_id)
    
    if date_from:
        query += ' AND p.payment_date >= %s'
        params.append(date_from)
    
    if date_to:
        query += ' AND p.payment_date <= %s'
        params.append(date_to)
    
    query += ' ORDER BY p.payment_date DESC, p.created_at DESC LIMIT %s'
    params.append(limit)
    
    cursor.execute(query, params)
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    return payments

def get_payment_by_id(payment_id):
    """Получить детальную информацию о погашении"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.payment_date, cl.name as client_name, p.somoni, p.dollar,
               p.exchange_rate, p.total_usd, p.notes, u.username, p.created_at
        FROM payments p
        LEFT JOIN clients cl ON p.client_id = cl.id
        LEFT JOIN users u ON p.created_by = u.user_id
        WHERE p.id = %s
    ''', (payment_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


# ============= ПАРТНЕРЫ =============

def add_partner(partner_date, client_id, somoni, exchange_rate, notes, created_by):
    """Добавить партнера"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Вычисляем общую сумму в долларах: сомони / курс
        total_usd = somoni / exchange_rate
        
        cursor.execute('''
            INSERT INTO partners 
            (partner_date, client_id, somoni, exchange_rate, total_usd, notes, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (partner_date, client_id, somoni, exchange_rate, total_usd, notes, created_by))
        
        partner_id = cursor.fetchone()[0]
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, partner_id
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)

def get_partners(limit=50, client_id=None, date_from=None, date_to=None):
    """Получить список партнеров с фильтрами"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT p.id, p.partner_date, cl.name as client_name, p.somoni,
               p.exchange_rate, p.total_usd, p.notes, u.username
        FROM partners p
        LEFT JOIN clients cl ON p.client_id = cl.id
        LEFT JOIN users u ON p.created_by = u.user_id
        WHERE 1=1
    '''
    
    params = []
    
    if client_id:
        query += ' AND p.client_id = %s'
        params.append(client_id)
    
    if date_from:
        query += ' AND p.partner_date >= %s'
        params.append(date_from)
    
    if date_to:
        query += ' AND p.partner_date <= %s'
        params.append(date_to)
    
    query += ' ORDER BY p.partner_date DESC, p.id DESC LIMIT %s'
    params.append(limit)
    
    cursor.execute(query, params)
    partners = cursor.fetchall()
    cursor.close()
    conn.close()
    return partners

def get_partner_by_id(partner_id):
    """Получить детальную информацию о партнере"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.partner_date, cl.name as client_name, p.somoni,
               p.exchange_rate, p.total_usd, p.notes, u.username, p.created_at
        FROM partners p
        LEFT JOIN clients cl ON p.client_id = cl.id
        LEFT JOIN users u ON p.created_by = u.user_id
        WHERE p.id = %s
    ''', (partner_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


# ============= УДАЛЕНИЕ ЗАПИСЕЙ (ТОЛЬКО ДЛЯ АДМИНОВ) =============

def delete_arrival(arrival_id):
    """Удалить запись прихода"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM arrivals WHERE id = %s', (arrival_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Запись прихода удалена"
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)

def delete_departure(departure_id):
    """Удалить запись расхода"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM departures WHERE id = %s', (departure_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Запись расхода удалена"
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)

def delete_payment(payment_id):
    """Удалить запись погашения"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM payments WHERE id = %s', (payment_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Запись погашения удалена"
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)

def delete_partner(partner_id):
    """Удалить запись партнера"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM partners WHERE id = %s', (partner_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Запись партнера удалена"
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, str(e)


def get_inventory_by_warehouse_and_firm():
    """Получить остатки с группировкой по складам и фирмам"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        WITH arrivals_data AS (
            SELECT 
                w.name as warehouse_name,
                f.name as firm_name,
                a.product_name,
                a.warehouse_id,
                a.firm_id,
                SUM(a.quantity_actual) as total_arrivals
            FROM arrivals a
            LEFT JOIN warehouses w ON a.warehouse_id = w.id
            LEFT JOIN firms f ON a.firm_id = f.id
            GROUP BY w.name, f.name, a.product_name, a.warehouse_id, a.firm_id
        ),
        departures_data AS (
            SELECT 
                d.warehouse_id,
                d.firm_id,
                d.product_name,
                SUM(d.quantity) as total_departures
            FROM departures d
            GROUP BY d.warehouse_id, d.firm_id, d.product_name
        )
        SELECT 
            ad.warehouse_name,
            ad.firm_name,
            ad.product_name,
            ad.total_arrivals - COALESCE(dd.total_departures, 0) as balance
        FROM arrivals_data ad
        LEFT JOIN departures_data dd 
            ON ad.warehouse_id = dd.warehouse_id 
            AND ad.firm_id = dd.firm_id 
            AND ad.product_name = dd.product_name
        WHERE ad.total_arrivals - COALESCE(dd.total_departures, 0) > 0
        ORDER BY ad.warehouse_name, ad.firm_name, ad.product_name
    ''')
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_inventory_by_warehouse_and_firm_for_group(warehouse_group_id):
    """Получить остатки с группировкой по складам и фирмам для группы складов"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        WITH arrivals_data AS (
            SELECT 
                w.name as warehouse_name,
                f.name as firm_name,
                a.product_name,
                a.warehouse_id,
                a.firm_id,
                SUM(a.quantity_actual) as total_arrivals
            FROM arrivals a
            LEFT JOIN warehouses w ON a.warehouse_id = w.id
            LEFT JOIN firms f ON a.firm_id = f.id
            WHERE w.group_id = %s
            GROUP BY w.name, f.name, a.product_name, a.warehouse_id, a.firm_id
        ),
        departures_data AS (
            SELECT 
                d.warehouse_id,
                d.firm_id,
                d.product_name,
                SUM(d.quantity) as total_departures
            FROM departures d
            JOIN warehouses w ON d.warehouse_id = w.id
            WHERE w.group_id = %s
            GROUP BY d.warehouse_id, d.firm_id, d.product_name
        )
        SELECT 
            ad.warehouse_name,
            ad.firm_name,
            ad.product_name,
            ad.total_arrivals - COALESCE(dd.total_departures, 0) as balance
        FROM arrivals_data ad
        LEFT JOIN departures_data dd 
            ON ad.warehouse_id = dd.warehouse_id 
            AND ad.firm_id = dd.firm_id 
            AND ad.product_name = dd.product_name
        WHERE ad.total_arrivals - COALESCE(dd.total_departures, 0) > 0
        ORDER BY ad.warehouse_name, ad.firm_name, ad.product_name
    ''', (warehouse_group_id, warehouse_group_id))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_inventory_by_warehouse_and_firm_for_user(user_id):
    """Получить остатки с группировкой по складам и фирмам для пользователя"""
    role, warehouse_group_id, is_active = get_user_role(user_id)
    
    if not is_active:
        return []
    
    # Админ видит все остатки
    if role == 'admin':
        return get_inventory_by_warehouse_and_firm()
    
    # Остальные видят только остатки своей группы складов
    if warehouse_group_id:
        return get_inventory_by_warehouse_and_firm_for_group(warehouse_group_id)
    
    return []


def get_summary_stats(year=None):
    """Получить сводную статистику за год"""
    from datetime import datetime
    
    if year is None:
        year = datetime.now().year
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Общий приход за год
    cursor.execute('''
        SELECT COALESCE(SUM(quantity_actual), 0)
        FROM arrivals
        WHERE EXTRACT(YEAR FROM arrival_date) = %s
    ''', (year,))
    total_arrivals = cursor.fetchone()[0]
    
    # Общий расход за год
    cursor.execute('''
        SELECT COALESCE(SUM(quantity), 0)
        FROM departures
        WHERE EXTRACT(YEAR FROM departure_date) = %s
    ''', (year,))
    total_departures = cursor.fetchone()[0]
    
    # Текущий остаток (реальный расчет на основе всех приходов и расходов)
    cursor.execute('''
        SELECT 
            COALESCE(SUM(arrivals), 0) - COALESCE(SUM(departures), 0) as balance
        FROM (
            SELECT SUM(quantity_actual) as arrivals, 0 as departures
            FROM arrivals
            
            UNION ALL
            
            SELECT 0 as arrivals, SUM(quantity) as departures
            FROM departures
        ) combined
    ''')
    current_balance = cursor.fetchone()[0]
    
    # Сумма продаж за год (только продажи клиентам)
    cursor.execute('''
        SELECT COALESCE(SUM(total), 0)
        FROM departures
        WHERE client_id IS NOT NULL AND EXTRACT(YEAR FROM departure_date) = %s
    ''', (year,))
    total_sales_year = cursor.fetchone()[0]
    
    # Оплачено за год (погашения)
    cursor.execute('''
        SELECT COALESCE(SUM(total_usd), 0)
        FROM payments
        WHERE EXTRACT(YEAR FROM payment_date) = %s
    ''', (year,))
    total_paid_year = cursor.fetchone()[0]
    
    # Общая сумма продаж за все время (только продажи клиентам)
    cursor.execute('''
        SELECT COALESCE(SUM(total), 0)
        FROM departures
        WHERE client_id IS NOT NULL
    ''')
    total_sales_all = cursor.fetchone()[0]
    
    # Общая сумма оплачено за все время
    cursor.execute('''
        SELECT COALESCE(SUM(total_usd), 0)
        FROM payments
    ''')
    total_paid_all = cursor.fetchone()[0]
    
    # Общий долг - правильный расчет: сумма долгов всех клиентов
    cursor.execute('''
        WITH client_sales AS (
            SELECT 
                d.client_id,
                COALESCE(SUM(d.total), 0) as sales
            FROM departures d
            WHERE d.client_id IS NOT NULL
            GROUP BY d.client_id
        ),
        client_payments AS (
            SELECT 
                p.client_id,
                COALESCE(SUM(p.total_usd), 0) as payments
            FROM payments p
            GROUP BY p.client_id
        )
        SELECT COALESCE(SUM(cs.sales - COALESCE(cp.payments, 0)), 0)
        FROM client_sales cs
        LEFT JOIN client_payments cp ON cs.client_id = cp.client_id
        WHERE cs.sales - COALESCE(cp.payments, 0) > 0
    ''')
    total_debt = cursor.fetchone()[0]
    
    # Количество должников (клиенты с долгом за все время)
    cursor.execute('''
        WITH client_sales AS (
            SELECT 
                d.client_id,
                COALESCE(SUM(d.total), 0) as sales
            FROM departures d
            WHERE d.client_id IS NOT NULL
            GROUP BY d.client_id
        ),
        client_payments AS (
            SELECT 
                p.client_id,
                COALESCE(SUM(p.total_usd), 0) as payments
            FROM payments p
            GROUP BY p.client_id
        )
        SELECT COUNT(*)
        FROM client_sales cs
        LEFT JOIN client_payments cp ON cs.client_id = cp.client_id
        WHERE cs.sales > COALESCE(cp.payments, 0)
    ''')
    debtors_count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return {
        'total_arrivals': float(total_arrivals),
        'total_departures': float(total_departures),
        'current_balance': float(current_balance),
        'total_sales': float(total_sales_year),
        'total_paid': float(total_paid_year),
        'total_debt': float(total_debt),
        'debtors_count': int(debtors_count)
    }

def get_summary_stats_by_warehouse_group(warehouse_group_id, year=None):
    """Получить сводную статистику по группе складов за год"""
    from datetime import datetime
    
    if year is None:
        year = datetime.now().year
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Общий приход
    cursor.execute('''
        SELECT COALESCE(SUM(a.quantity_actual), 0)
        FROM arrivals a
        JOIN warehouses w ON a.warehouse_id = w.id
        WHERE w.group_id = %s AND EXTRACT(YEAR FROM a.arrival_date) = %s
    ''', (warehouse_group_id, year))
    total_arrivals = cursor.fetchone()[0]
    
    # Общий расход
    cursor.execute('''
        SELECT COALESCE(SUM(d.quantity), 0)
        FROM departures d
        JOIN warehouses w ON d.warehouse_id = w.id
        WHERE w.group_id = %s AND EXTRACT(YEAR FROM d.departure_date) = %s
    ''', (warehouse_group_id, year))
    total_departures = cursor.fetchone()[0]
    
    # Текущий остаток по группе
    cursor.execute('''
        SELECT COALESCE(SUM(arrivals), 0) - COALESCE(SUM(departures), 0)
        FROM (
            SELECT SUM(a.quantity_actual) as arrivals, 0 as departures
            FROM arrivals a
            JOIN warehouses w ON a.warehouse_id = w.id
            WHERE w.group_id = %s
            
            UNION ALL
            
            SELECT 0 as arrivals, SUM(d.quantity) as departures
            FROM departures d
            JOIN warehouses w ON d.warehouse_id = w.id
            WHERE w.group_id = %s
        ) combined
    ''', (warehouse_group_id, warehouse_group_id))
    current_balance = cursor.fetchone()[0]
    
    # Сумма продаж за год (только продажи клиентам)
    cursor.execute('''
        SELECT COALESCE(SUM(d.total), 0)
        FROM departures d
        JOIN warehouses w ON d.warehouse_id = w.id
        WHERE w.group_id = %s AND d.client_id IS NOT NULL AND EXTRACT(YEAR FROM d.departure_date) = %s
    ''', (warehouse_group_id, year))
    total_sales_year = cursor.fetchone()[0]
    
    # Оплачено за год (погашения за год)
    cursor.execute('''
        SELECT COALESCE(SUM(total_usd), 0)
        FROM payments
        WHERE EXTRACT(YEAR FROM payment_date) = %s
    ''', (year,))
    total_paid_year = cursor.fetchone()[0]
    
    # Общая сумма продаж за все время по группе (только продажи клиентам)
    cursor.execute('''
        SELECT COALESCE(SUM(d.total), 0)
        FROM departures d
        JOIN warehouses w ON d.warehouse_id = w.id
        WHERE w.group_id = %s AND d.client_id IS NOT NULL
    ''', (warehouse_group_id,))
    total_sales_all = cursor.fetchone()[0]
    
    # Общая сумма оплачено за все время
    cursor.execute('''
        SELECT COALESCE(SUM(total_usd), 0)
        FROM payments
    ''')
    total_paid_all = cursor.fetchone()[0]
    
    # Общий долг - правильный расчет: сумма долгов всех клиентов
    cursor.execute('''
        WITH client_sales AS (
            SELECT 
                d.client_id,
                COALESCE(SUM(d.total), 0) as sales
            FROM departures d
            WHERE d.client_id IS NOT NULL
            GROUP BY d.client_id
        ),
        client_payments AS (
            SELECT 
                p.client_id,
                COALESCE(SUM(p.total_usd), 0) as payments
            FROM payments p
            GROUP BY p.client_id
        )
        SELECT COALESCE(SUM(cs.sales - COALESCE(cp.payments, 0)), 0)
        FROM client_sales cs
        LEFT JOIN client_payments cp ON cs.client_id = cp.client_id
        WHERE cs.sales - COALESCE(cp.payments, 0) > 0
    ''')
    total_debt = cursor.fetchone()[0]
    
    # Количество должников
    cursor.execute('''
        WITH client_sales AS (
            SELECT 
                d.client_id,
                COALESCE(SUM(d.total), 0) as sales
            FROM departures d
            WHERE d.client_id IS NOT NULL
            GROUP BY d.client_id
        ),
        client_payments AS (
            SELECT 
                p.client_id,
                COALESCE(SUM(p.total_usd), 0) as payments
            FROM payments p
            GROUP BY p.client_id
        )
        SELECT COUNT(*)
        FROM client_sales cs
        LEFT JOIN client_payments cp ON cs.client_id = cp.client_id
        WHERE cs.sales > COALESCE(cp.payments, 0)
    ''')
    debtors_count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return {
        'total_arrivals': float(total_arrivals),
        'total_departures': float(total_departures),
        'current_balance': float(current_balance),
        'total_sales': float(total_sales_year),
        'total_paid': float(total_paid_year),
        'total_debt': float(total_debt),
        'debtors_count': int(debtors_count)
    }

def get_summary_stats_by_user(user_id, year=None):
    """Получить сводную статистику доступную пользователю"""
    role, warehouse_group_id, is_active = get_user_role(user_id)
    
    if not is_active:
        return None
    
    # Админ видит всю статистику
    if role == 'admin':
        return get_summary_stats(year)
    
    # Остальные видят только статистику своей группы складов
    if warehouse_group_id:
        return get_summary_stats_by_warehouse_group(warehouse_group_id, year)
    
    return None


def get_client_debts(year=None):
    """Получить список должников с детальной информацией"""
    from datetime import datetime
    
    if year is None:
        year = datetime.now().year
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        WITH client_sales AS (
            SELECT 
                d.client_id,
                c.name as client_name,
                COALESCE(SUM(d.total), 0) as total_sales
            FROM departures d
            LEFT JOIN clients c ON d.client_id = c.id
            WHERE d.client_id IS NOT NULL
            GROUP BY d.client_id, c.name
        ),
        client_payments AS (
            SELECT 
                p.client_id,
                COALESCE(SUM(p.total_usd), 0) as total_paid
            FROM payments p
            GROUP BY p.client_id
        )
        SELECT 
            cs.client_id,
            cs.client_name,
            cs.total_sales,
            COALESCE(cp.total_paid, 0) as total_paid,
            cs.total_sales - COALESCE(cp.total_paid, 0) as debt
        FROM client_sales cs
        LEFT JOIN client_payments cp ON cs.client_id = cp.client_id
        WHERE cs.total_sales - COALESCE(cp.total_paid, 0) > 0
        ORDER BY (cs.total_sales - COALESCE(cp.total_paid, 0)) DESC
    ''')
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return results

def get_client_debts_by_warehouse_group(warehouse_group_id, year=None):
    """Получить список должников по группе складов"""
    from datetime import datetime
    
    if year is None:
        year = datetime.now().year
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        WITH client_sales AS (
            SELECT 
                d.client_id,
                c.name as client_name,
                COALESCE(SUM(d.total), 0) as total_sales
            FROM departures d
            LEFT JOIN clients c ON d.client_id = c.id
            JOIN warehouses w ON d.warehouse_id = w.id
            WHERE d.client_id IS NOT NULL AND w.group_id = %s
            GROUP BY d.client_id, c.name
        ),
        client_payments AS (
            SELECT 
                p.client_id,
                COALESCE(SUM(p.total_usd), 0) as total_paid
            FROM payments p
            GROUP BY p.client_id
        )
        SELECT 
            cs.client_id,
            cs.client_name,
            cs.total_sales,
            COALESCE(cp.total_paid, 0) as total_paid,
            cs.total_sales - COALESCE(cp.total_paid, 0) as debt
        FROM client_sales cs
        LEFT JOIN client_payments cp ON cs.client_id = cp.client_id
        WHERE cs.total_sales - COALESCE(cp.total_paid, 0) > 0
        ORDER BY (cs.total_sales - COALESCE(cp.total_paid, 0)) DESC
    ''', (warehouse_group_id,))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return results

def get_client_debts_by_user(user_id, year=None):
    """Получить список должников доступный пользователю"""
    role, warehouse_group_id, is_active = get_user_role(user_id)
    
    if not is_active:
        return []
    
    # Админ видит всех должников
    if role == 'admin':
        return get_client_debts(year)
    
    # Остальные видят только должников своей группы складов
    if warehouse_group_id:
        return get_client_debts_by_warehouse_group(warehouse_group_id, year)
    
    return []
