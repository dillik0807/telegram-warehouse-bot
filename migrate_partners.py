import psycopg2
from config import DATABASE_URL

def migrate():
    """Создание таблицы партнеров"""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Создаем таблицу партнеров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partners (
            id SERIAL PRIMARY KEY,
            partner_date DATE NOT NULL,
            client_id INTEGER REFERENCES clients(id),
            somoni DECIMAL(15, 2) DEFAULT 0,
            exchange_rate DECIMAL(10, 4) NOT NULL,
            total_usd DECIMAL(15, 2) NOT NULL,
            notes TEXT,
            created_by BIGINT REFERENCES users(user_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Таблица партнеров создана успешно!")

if __name__ == '__main__':
    migrate()
