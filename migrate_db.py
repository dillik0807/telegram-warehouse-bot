"""
Скрипт миграции базы данных для добавления недостающих колонок и таблиц
"""
import psycopg2
from config import DATABASE_URL

def migrate():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        print("=" * 60)
        print("Начало миграции базы данных")
        print("=" * 60)
        
        # 1. Создаем таблицу warehouse_groups если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS warehouse_groups (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица warehouse_groups создана/проверена")
        
        # 2. Создаем таблицу warehouses если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS warehouses (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица warehouses создана/проверена")
        
        # 3. Проверяем и добавляем колонку group_id в warehouses
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='warehouses' AND column_name='group_id'
        """)
        
        if not cursor.fetchone():
            cursor.execute('''
                ALTER TABLE warehouses 
                ADD COLUMN group_id INTEGER REFERENCES warehouse_groups(id)
            ''')
            print("✅ Колонка group_id добавлена в таблицу warehouses")
        else:
            print("✅ Колонка group_id уже существует в warehouses")
        
        # 4. Создаем таблицу products если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица products создана/проверена")
        
        # 5. Создаем таблицу transactions если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                type TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица transactions создана/проверена")
        
        # 6. Создаем таблицу admins если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                user_id BIGINT PRIMARY KEY,
                username TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица admins создана/проверена")
        
        # 7. Создаем таблицу firms если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS firms (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица firms создана/проверена")
        
        # 8. Создаем таблицу clients если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица clients создана/проверена")
        
        # 9. Создаем таблицу prices если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                id SERIAL PRIMARY KEY,
                product_name TEXT NOT NULL UNIQUE,
                price DECIMAL(10, 2) NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица prices создана/проверена")
        
        # 10. Создаем таблицу coalitions если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coalitions (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица coalitions создана/проверена")
        
        conn.commit()
        print("\n" + "=" * 60)
        print("✅ Миграция успешно завершена!")
        print("=" * 60)
        
        # Показываем статистику
        print("\nСтатистика базы данных:")
        tables = ['warehouse_groups', 'warehouses', 'products', 'transactions', 
                  'admins', 'firms', 'clients', 'prices', 'coalitions']
        
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            print(f"  📊 {table}: {count} записей")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Ошибка миграции: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    migrate()
