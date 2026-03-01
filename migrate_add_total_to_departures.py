import psycopg2
from config import DATABASE_URL

def migrate():
    """Добавить поле total в таблицу departures и пересчитать существующие записи"""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        # Проверяем, существует ли уже колонка total
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='departures' AND column_name='total'
        """)
        
        if cursor.fetchone() is None:
            print("Добавляем колонку total в таблицу departures...")
            cursor.execute("""
                ALTER TABLE departures 
                ADD COLUMN total DECIMAL(10, 2) DEFAULT 0
            """)
            
            # Пересчитываем total для существующих записей по формуле: (quantity / 20) * price
            print("Пересчитываем total для существующих записей...")
            cursor.execute("""
                UPDATE departures 
                SET total = (quantity / 20) * price
            """)
            
            conn.commit()
            print("✅ Миграция завершена успешно!")
            print("   - Добавлена колонка total")
            print("   - Пересчитаны все существующие записи по формуле: (quantity / 20) * price")
        else:
            print("⚠️ Колонка total уже существует")
            # Все равно пересчитываем на случай если формула была неправильной
            print("Пересчитываем total для всех записей...")
            cursor.execute("""
                UPDATE departures 
                SET total = (quantity / 20) * price
            """)
            conn.commit()
            print("✅ Пересчет завершен!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        print(f"❌ Ошибка миграции: {e}")
        raise

if __name__ == '__main__':
    migrate()
