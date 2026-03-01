"""
Миграция для добавления детальной информации о приходе товара
"""
import psycopg2
from config import DATABASE_URL

def migrate_arrival_details():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        print("=" * 60)
        print("Миграция детального учета прихода")
        print("=" * 60)
        
        # 1. Создаем таблицу arrivals для детального учета прихода
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS arrivals (
                id SERIAL PRIMARY KEY,
                arrival_date DATE NOT NULL,
                wagon_number TEXT,
                firm_id INTEGER REFERENCES firms(id),
                warehouse_id INTEGER REFERENCES warehouses(id),
                product_name TEXT NOT NULL,
                source TEXT,
                quantity_document INTEGER NOT NULL,
                quantity_actual INTEGER NOT NULL,
                notes TEXT,
                created_by BIGINT REFERENCES users(user_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Таблица arrivals создана")
        
        # 2. Добавляем индексы для быстрого поиска
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_arrivals_date 
            ON arrivals(arrival_date)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_arrivals_warehouse 
            ON arrivals(warehouse_id)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_arrivals_firm 
            ON arrivals(firm_id)
        ''')
        print("✅ Индексы созданы")
        
        conn.commit()
        print("\n" + "=" * 60)
        print("✅ Миграция успешно завершена!")
        print("=" * 60)
        
        print("\nНовые поля для прихода товара:")
        print("  📅 Дата прихода")
        print("  🚂 № Вагона")
        print("  🏭 Фирма")
        print("  🏢 Склад")
        print("  📦 Товар")
        print("  📄 Количество по документу")
        print("  ✅ Количество по факту")
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
    migrate_arrival_details()
