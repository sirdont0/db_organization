#!/usr/local/bin/python3.11

import psycopg2
from tabulate import tabulate

def connect_db():
    return psycopg2.connect(
             user="postgres",
             password="12345678",
             host="192.168.1.118",
             #host="DESKTOP-0U9DGT4",
             port="5433",
             #database="organization",
             database="test",
             connect_timeout=10
    )
    
def fetch_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cur.fetchall()
    conn.close()
    return [table[0] for table in tables]

def fetch_data(table):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    conn.close()
    return rows, colnames

def show_titles(tables):
    i = 1
    for table in tables:
        print(i, table)
        i += 1
    print(i, 'menu')
    print()

def insert_data(table, columns, values):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})", values)
        conn.commit()
    except psycopg2.DatabaseError as e:
        print(e)
        
    finally:
        if conn:
            conn.close()

def update_data(table, columns, values, row_id, id):
    conn = connect_db()
    cur = conn.cursor()
    set_clause = ', '.join([f"{col}=%s" for col in columns])
    cur.execute(f"UPDATE {table} SET {set_clause} WHERE {row_id} = {id}", values)
    conn.commit()
    conn.close()

def delete_data(table, row_id, id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table} WHERE {row_id} = {id} CASCADE;")
    conn.commit()
    conn.close()

# Пример использования функций
def main():
    print()
    while True:
        print()
        print('Выбери номер действия: ')
        print()
        print('1 Просмотр данных')
        print('2 Добавление данных')
        print('3 Изменение данных')
        print('4 Удаление данных')
        print()
        print('Для выхода напишите exit')
        print()
        choice = input()
        print()
        if str(choice) == '1':
            while True:
                print('Какую таблицу просмотреть: ')
                show_titles(fetch_tables()) 
                choice_show = input('Введи название таблицы: ')
                if choice_show in fetch_tables():
                    print()
                    rows, colnames = fetch_data(choice_show)
                    print(tabulate(rows, headers=colnames, tablefmt='pretty'))
                    print()
                elif choice_show == 'menu':
                    break
                else:
                    print('Неверное название!')
                    print()

        elif str(choice) == '2':
             while True:
                print('В какую таблицу добавить данные: ')
                show_titles(fetch_tables()) 
                choice_show = input('Введи название таблицы: ')
                if choice_show in fetch_tables():
                    adding = []
                    print()
                    rows, colnames = fetch_data(choice_show)
                    for data in range(len(colnames)):
                        value = input(f"Введите {colnames[data]}: ")
                        adding.append(value)
                    insert_data(choice_show, colnames, adding)
                    print()
                elif choice_show == 'menu':
                    break
                else:
                    print('Неверное название!')
                    print()
        elif str(choice) == '3':
             while True:
                print('В какую таблицу внести изменения: ')
                choice_col = []
                choice_values = []
                show_titles(fetch_tables()) 
                choice_show = input('Введи название таблицы: ')
                if choice_show in fetch_tables():
                    print()
                    rows, colnames = fetch_data(choice_show)
                    print(tabulate(rows, headers=colnames, tablefmt='pretty'))
                    print()
                    try:
                        choice_id = input('Введите id записи, которую хотите изменить: ')
                        choice_col_non = input('Введите названия стобцов через запятую без пробелов, которые хотите изменить: ')
                        choice_col = choice_col_non.split(',')
                        choice_values_non = input('Введите соответсвенно значения через запятую без пробелов, на которые хотите изменить: ')
                        choice_values = choice_values_non.split(',')
                        update_data(choice_show, choice_col, choice_values, colnames[0], choice_id)
                        print()
                    except psycopg2.DatabaseError as e:
                        print(e)
                    finally:
                        print()
                elif choice_show == 'menu':
                    break
                else:
                    print('Неверное название!')
                    print()
        elif str(choice) == '4':
            while True:
                print('В какой таблице хотите удалить значения: ')
                show_titles(fetch_tables()) 
                choice_show = input('Введи название таблицы: ')
                if choice_show in fetch_tables():
                    print()
                    rows, colnames = fetch_data(choice_show)
                    print(tabulate(rows, headers=colnames, tablefmt='pretty'))
                    print()
                    try:
                        choice_id = input('Введите id записи, которую хотите удалить: ')
                        delete_data(choice_show, colnames[0], choice_id)
                    except psycopg2.DatabaseError as e:
                        print(e)
                    finally:
                        print()
                elif choice_show == 'menu':
                    break
                else:
                    print('Неверное название!')
                    print()
        elif str(choice) == 'exit':
            exit()
        else:
            print('Выбери корректное значение!')

if __name__ == "__main__":
    main()
