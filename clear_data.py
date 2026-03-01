"""
Скрипт для очистки данных приходов и расходов
ВНИМАНИЕ: Это удалит ВСЕ данные из таблиц arrivals и departures!
"""

import psycopg2
from config import DATABASE_URL

def clear_arrivals_and_departures():
    """Очистить таблицы arrivals и departures"""
    
    print("⚠️  ВНИМАНИЕ! Это удалит ВСЕ данные из таблиц:")
    print("   - arrivals (приходы)")
    print("   - departures (расходы)")
    print()
    
    confirm = input("Вы уверены? Введите 'ДА' для подтверждения: ")
    
    if confirm != 'ДА':
        print("❌ Отменено")
        return
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
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
        
        # Сбрасываем счетчики ID (опционально)
        print("\n🔄 Сброс счетчиков ID...")
        cursor.execute('ALTER SEQUENCE arrivals_id_seq RESTART WITH 1')
        cursor.execute('ALTER SEQUENCE departures_id_seq RESTART WITH 1')
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Данные успешно очищены!")
        print(f"   Arrivals: {arrivals_count} записей удалено")
        print(f"   Departures: {departures_count} записей удалено")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        if conn:
            conn.rollback()

if __name__ == '__main__':
    clear_arrivals_and_departures()
