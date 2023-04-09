"""Скрипт для заполнения данными таблиц в БД Postgres."""

# делаем требуемые импорты
import psycopg2
import psycopg2.errors
import csv

# connect to DATABASE north

conn = psycopg2.connect(host="localhost",
                        database="north",
                        user="postgres",
                        password="bdfy09111994")

try:
    with conn:
        with conn.cursor() as cur:
            # Заполняем данными таблицу employees
            with open("north_data/employees_data.csv") as file:
                rows = csv.DictReader(file)
                id = 1
                for row in rows:
                    cur.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)",
                                (
                                    id, row['first_name'], row['last_name'], row['title'], row['birth_date'],
                                    row['notes']))
                    id += 1

            # Заполняем данными таблицу customers
            with open("north_data/customers_data.csv", encoding='cp1251') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cur.execute("INSERT INTO customers VALUES (%s, %s)",
                                (row['customer_id'], row['company_name']))

            # Заполняем данными таблицу orders
            with open("north_data/orders_data.csv", encoding='cp1251') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cur.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s)",
                                (row['order_id'], row['customer_id'], row['employee_id'], row['order_date'],
                                 row['ship_city']))

# Проверка существования данных в таблице
except psycopg2.errors.UniqueViolation:
    print("Данные ранее добавлены в таблицу")

finally:
    conn.close()
