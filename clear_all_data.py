"""
Скрипт для полной очистки данных: arrivals, departures, payments
"""

import psycopg2
from config import DATABASE_URL

def clear_all_data():
    """Очистить все таблицы с данными"""
    
    print("🗑️  Полная очистка данных...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Удаляем все записи из payments
        print("\n🗑️  Удаление данных из payments...")
        cursor.execute('DELETE FROM payments')
        payments_count = cursor.rowcount
        print(f"   Удалено записей: {payments_count}")
        
        # Удаляем все записи из partners
        print("\n🗑️  Удаление данных из partners...")
        cursor.execute('DELETE FROM partners')
        partners_count = cursor.rowcount
        print(f"   Удалено записей: {partners_count}")
        
        # Удаляем все записи из departures
        print("\n🗑️  Удаление данных из departures...")
        cursor.execute('DELETE FROM departures')
        departures_count = cursor.rowcount
        print(f"   Удалено записей: {departures_count}")
        
        # Удаляем все записи из arrivals
        print("\n🗑️  Удаление данных из arrivals...")
        cursor.execute('DELETE FROM arrivals')
        arrivals_count = cursor.rowcount
        print(f"   Удалено записей: {arrivals_count}")
        
        # Сбрасываем счетчики ID
        print("\n🔄 Сброс счетчиков ID...")
        cursor.execute('ALTER SEQUENCE arrivals_id_seq RESTART WITH 1')
        cursor.execute('ALTER SEQUENCE departures_id_seq RESTART WITH 1')
        cursor.execute('ALTER SEQUENCE payments_id_seq RESTART WITH 1')
        cursor.execute('ALTER SEQUENCE partners_id_seq RESTART WITH 1')
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Все данные успешно очищены!")
        print(f"   Arrivals: {arrivals_count} записей удалено")
        print(f"   Departures: {departures_count} записей удалено")
        print(f"   Payments: {payments_count} записей удалено")
        print(f"   Partners: {partners_count} записей удалено")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        if conn:
            conn.rollback()

if __name__ == '__main__':
    clear_all_data()
