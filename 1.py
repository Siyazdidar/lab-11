import psycopg2
from tabulate import tabulate
import re

conn = psycopg2.connect(host="localhost", dbname="lab10", user="postgres", password="1", port=5432)
cur = conn.cursor()

def insert_or_update_user(name, surname, phone):
    cur.execute("SELECT 1 FROM PhoneBook WHERE name = %s AND surname = %s", (name, surname))
    if cur.fetchone():
        cur.execute("UPDATE PhoneBook SET phone = %s WHERE name = %s AND surname = %s", (phone, name, surname))
    else:
        cur.execute("INSERT INTO PhoneBook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
    conn.commit()

def insert_many_users():
    invalid_entries = []
    while True:
        name = input('Name ("b" to back): ')
        if name.lower() == 'b':
            break
        surname = input('Surname: ')
        phone = input('Phone: ')
        invalid_entries.append((name, surname, phone))
    if invalid_entries:
        print("Invalid entries:")
        print(tabulate(invalid_entries, headers=["Name", "Surname", "Phone"], tablefmt='grid'))

def search_by_pattern():
    pattern = input('Enter pattern to search (name, surname or phone): ')
    cur.execute("""
        SELECT * FROM PhoneBook
        WHERE name ILIKE %s OR surname ILIKE %s OR phone ILIKE %s
    """, (f"%{pattern}%", f"%{pattern}%", f"%{pattern}%"))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))

def delete_user():
    key = input('Delete by "name" or "phone": ')
    if key == "name":
        name = input("Enter name: ")
        surname = input("Enter surname: ")
        cur.execute("DELETE FROM PhoneBook WHERE name = %s AND surname = %s", (name, surname))
    elif key == "phone":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (phone,))
    conn.commit()

def see_table():
    cur.execute("SELECT * FROM PhoneBook")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))

def paginate():
    limit = int(input("Enter limit (number of rows per page): "))
    offset = int(input("Enter offset (starting row): "))
    cur.execute("SELECT * FROM PhoneBook ORDER BY user_id LIMIT %s OFFSET %s", (limit, offset))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))

def main():
    while True:
        print("""
1. I - INSERT or UPDATE single user
2. M - INSERT many users with validation
3. Q - QUERY by pattern
4. D - DELETE user by name or phone
5. S - SEE all users
6. P - PAGINATE view
7. C - CLOSE
        """)
        command = input("Choose an option: ").lower()

        if command == 'i':
            name = input("Name: ")
            surname = input("Surname: ")
            phone = input("Phone: ")
            insert_or_update_user(name, surname, phone)

        elif command == 'm':
            insert_many_users()

        elif command == 'q':
            search_by_pattern()

        elif command == 'd':
            delete_user()

        elif command == 's':
            see_table()

        elif command == 'p':
            paginate()

        elif command == 'c':
            break

main()
cur.close()
conn.close()
