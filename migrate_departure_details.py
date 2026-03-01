"""
Миграция для добавления детальной информации о выводе товара
"""
import psycopg2
from config import DATABASE_URL

def migrate_departure_details():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        print("=" * 60)
        print("Миграция детального учета вывода")
        print("=" * 60)
        
        # 1. Создаем таблицу departures для детального учета вывода
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departures (
                id SERIAL PRIMARY KEY,
                departure_date DATE NOT NULL,
                coalition_id INTEGER REFERENCES coalitions(id),
                firm_id INTEGER REFERENCES firms(id),
                warehouse_id INTEGER REFERENCES warehouses(id),
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10, 2),
                notes TEXT,
                created_by BIGINT REFERENCES users(user_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица departures создана")
        
        # 2. Добавляем индексы для быстрого поиска
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_departures_date 
            ON departures(departure_date)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_departures_warehouse 
            ON departures(warehouse_id)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_departures_coalition 
            ON departures(coalition_id)
        ''')
        print("✅ Индексы созданы")
        
        conn.commit()
        print("\n" + "=" * 60)
        print("✅ Миграция успешно завершена!")
        print("=" * 60)
        
        print("\nНовые поля для вывода товара:")
        print("  📅 Дата вывода")
        print("  📊 Коалица")
        print("  🏭 Фирма")
        print("  🏢 Склад")
        print("  📦 Товар")
        print("  📦 Количество")
        print("  💰 Цена")
        print("  📝 Примечания")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Ошибка миграции: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    migrate_departure_details()
