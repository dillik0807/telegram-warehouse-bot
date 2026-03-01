"""
Миграция для добавления системы логин/пароль
"""
import psycopg2
from config import DATABASE_URL

def migrate_login_system():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        print("=" * 60)
        print("Миграция системы логин/пароль")
        print("=" * 60)
        
        # 1. Добавляем колонки login и password в таблицу users
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='login'
        """)
        
        if not cursor.fetchone():
            cursor.execute('''
                ALTER TABLE users 
                ADD COLUMN login TEXT UNIQUE,
                ADD COLUMN password TEXT
            ''')
            print("✅ Колонки login и password добавлены")
        else:
            print("✅ Колонки login и password уже существуют")
        
        # 2. Создаем таблицу для сессий (связь telegram_id с user_id)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                telegram_id BIGINT PRIMARY KEY,
                user_id BIGINT REFERENCES users(user_id),
                logged_in_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица user_sessions создана")
        
        # 3. Обновляем существующих пользователей - создаем логины
        import hashlib
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        
        cursor.execute('''
            UPDATE users 
            SET login = 'admin', password = %s
            WHERE role = 'admin' AND login IS NULL
        ''', (password_hash,))
        print("✅ Для админов созданы логины по умолчанию (admin/admin123)")
        
        conn.commit()
        print("\n" + "=" * 60)
        print("✅ Миграция успешно завершена!")
        print("=" * 60)
        
        print("\nВажно:")
        print("  - Пользователи теперь входят через логин/пароль")
        print("  - Админ по умолчанию: login=admin, password=admin123")
        print("  - Рекомендуется сменить пароль после первого входа")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Ошибка миграции: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    migrate_login_system()
