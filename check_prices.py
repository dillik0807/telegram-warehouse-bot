"""
Проверка данных в таблице цен
"""
import psycopg2
from config import DATABASE_URL

def check_prices():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Проверяем существует ли таблица
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'prices'
        )
    """)
    table_exists = cursor.fetchone()[0]
    print(f"Таблица prices существует: {table_exists}")
    
    if table_exists:
        # Проверяем структуру таблицы
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'prices'
        """)
        columns = cursor.fetchall()
        print("\nСтруктура таблицы prices:")
        for col_name, col_type in columns:
            print(f"  - {col_name}: {col_type}")
        
        # Проверяем данные
        cursor.execute('SELECT * FROM prices')
        prices = cursor.fetchall()
        print(f"\nКоличество записей: {len(prices)}")
        if prices:
            print("\nДанные:")
            for price in prices:
                print(f"  {price}")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    check_prices()
