"""
Скрипт для проверки данных клиента
"""

import psycopg2
from config import DATABASE_URL

def check_client_data():
    """Проверить данные клиента"""
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("ПРОВЕРКА ДАННЫХ КЛИЕНТОВ")
    print("=" * 60)
    
    # Все расходы с клиентами
    print("\n📤 ВСЕ РАСХОДЫ С КЛИЕНТАМИ:")
    print("-" * 60)
    cursor.execute('''
        SELECT 
            d.id,
            d.departure_date,
            c.name as client_name,
            d.product_name,
            d.quantity,
            d.price,
            d.total
        FROM departures d
        LEFT JOIN clients c ON d.client_id = c.id
        WHERE d.client_id IS NOT NULL
        ORDER BY d.departure_date DESC
    ''')
    
    departures = cursor.fetchall()
    if departures:
        for dep in departures:
            dep_id, date, client, product, qty, price, total = dep
            print(f"ID: {dep_id}")
            print(f"  Дата: {date}")
            print(f"  Клиент: {client}")
            print(f"  Товар: {product}")
            print(f"  Количество: {qty}")
            print(f"  Цена: {price}")
            print(f"  Сумма: {total}")
            print()
    else:
        print("  Нет записей")
    
    # Все погашения
    print("\n💰 ВСЕ ПОГАШЕНИЯ:")
    print("-" * 60)
    cursor.execute('''
        SELECT 
            p.id,
            p.payment_date,
            c.name as client_name,
            p.somoni,
            p.exchange_rate,
            p.total_usd
        FROM payments p
        LEFT JOIN clients c ON p.client_id = c.id
        ORDER BY p.payment_date DESC
    ''')
    
    payments = cursor.fetchall()
    if payments:
        for pay in payments:
            pay_id, date, client, somoni, rate, total = pay
            print(f"ID: {pay_id}")
            print(f"  Дата: {date}")
            print(f"  Клиент: {client}")
            print(f"  Сомони: {somoni}")
            print(f"  Курс: {rate}")
            print(f"  Сумма $: {total}")
            print()
    else:
        print("  Нет записей")
    
    # Долги по клиентам
    print("\n💳 ДОЛГИ ПО КЛИЕНТАМ:")
    print("-" * 60)
    cursor.execute('''
        WITH client_sales AS (
            SELECT 
                d.client_id,
                c.name as client_name,
                COALESCE(SUM(d.total), 0) as total_sales
            FROM departures d
            LEFT JOIN clients c ON d.client_id = c.id
            WHERE d.client_id IS NOT NULL
            GROUP BY d.client_id, c.name
        ),
        client_payments AS (
            SELECT 
                p.client_id,
                COALESCE(SUM(p.total_usd), 0) as total_paid
            FROM payments p
            GROUP BY p.client_id
        )
        SELECT 
            cs.client_name,
            cs.total_sales,
            COALESCE(cp.total_paid, 0) as total_paid,
            cs.total_sales - COALESCE(cp.total_paid, 0) as debt
        FROM client_sales cs
        LEFT JOIN client_payments cp ON cs.client_id = cp.client_id
        ORDER BY cs.client_name
    ''')
    
    debts = cursor.fetchall()
    if debts:
        for debt in debts:
            client, sales, paid, debt_amount = debt
            print(f"Клиент: {client}")
            print(f"  Сумма продаж: {sales:.2f} $")
            print(f"  Оплачено: {paid:.2f} $")
            print(f"  Долг: {debt_amount:.2f} $")
            print()
    else:
        print("  Нет должников")
    
    cursor.close()
    conn.close()
    
    print("=" * 60)

if __name__ == '__main__':
    check_client_data()
