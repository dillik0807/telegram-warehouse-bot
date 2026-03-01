"""
Миграция для добавления клиента в таблицу departures
"""
import psycopg2
from config import DATABASE_URL

def migrate_add_client():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        print("=" * 60)
        print("Добавление клиента в departures")
        print("=" * 60)
        
        # Добавляем поле client_id в таблицу departures
        cursor.execute('''
            ALTER TABLE departures 
            ADD COLUMN IF NOT EXISTS client_id INTEGER REFERENCES clients(id)
        ''')
        print("✅ Поле client_id добавлено в таблицу departures")
        
        # Добавляем индекс
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_departures_client 
            ON departures(client_id)
        ''')
        print("✅ Индекс создан")
        
        conn.commit()
        print("\n" + "=" * 60)
        print("✅ Миграция успешно завершена!")
        print("=" * 60)
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Ошибка миграции: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    migrate_add_client()
