"""
Миграция для добавления системы ролей пользователей
"""
import psycopg2
from config import DATABASE_URL

def migrate_roles():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        print("=" * 60)
        print("Миграция системы ролей")
        print("=" * 60)
        
        # 1. Создаем новую таблицу users с ролями
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
        print("✅ Таблица users создана")
        
        # 2. Переносим данные из admins в users с ролью 'admin'
        cursor.execute('''
            INSERT INTO users (user_id, username, role, added_at)
            SELECT user_id, username, 'admin', added_at
            FROM admins
            ON CONFLICT (user_id) DO NOTHING
        ''')
        print("✅ Данные из admins перенесены в users")
        
        # 3. Создаем таблицу для логов доступа
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_logs (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица access_logs создана")
        
        conn.commit()
        print("\n" + "=" * 60)
        print("✅ Миграция ролей успешно завершена!")
        print("=" * 60)
        
        # Показываем статистику
        print("\nДоступные роли:")
        print("  👑 admin - Управляющий (полный доступ)")
        print("  📊 manager - Менеджер (управление товарами)")
        print("  🏢 warehouse_manager - Завсклад (управление складом)")
        print("  💰 cashier - Кассир (только просмотр и продажи)")
        
        cursor.execute('SELECT COUNT(*), role FROM users GROUP BY role')
        stats = cursor.fetchall()
        print("\nТекущие пользователи:")
        for count, role in stats:
            print(f"  {role}: {count} пользователей")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Ошибка миграции: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    migrate_roles()
