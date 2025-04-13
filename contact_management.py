import mysql.connector
from mysql.connector import Error
import os


class Contact:
    def __init__(self, contact_name, phone_number, email, address):
        self.contact_name = contact_name
        self.phone_number = phone_number
        self.email = email
        self.address = address


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password= os.getenv('Password'),
            database= os.getenv('database_name')
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def add_contact(connection, contact):
    cursor = connection.cursor()
    query = """INSERT INTO contacts (contact_name, phone_number, email, address) 
            VALUES (%s, %s, %s, %s)"""
    cursor.execute(query, (contact.contact_name, contact.phone_number, contact.email, contact.address))
    connection.commit()


def view_contacts(connection):
    print("CONTACTS:- ")
    cursor = connection.cursor()
    cursor.execute("SELECT contact_name, phone_number FROM contacts")
    for (contact_name, phone_number) in cursor:
        print(f"Name: {contact_name}, Phone: {phone_number}")


def search_contact(connection, search_term):
    cursor = connection.cursor()
    query = """SELECT contact_name, phone_number, email, address FROM contacts 
            WHERE contact_name LIKE %s OR phone_number LIKE %s"""
    cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
    for (contact_name, phone_number, email, address) in cursor:
        print(f"Found Contact - Name: {contact_name}, Phone: {phone_number}, Email: {email}, Address: {address}")
        break
    else:
        print("No contact found, Please enter correct contact name or phone number.")


def update_contact(connection, contact_name, phone_number=None, email=None, address=None):
    cursor = connection.cursor()
    query = "UPDATE contacts SET "
    fields = []
    values = []
    if phone_number:
        fields.append("phone_number = %s")
        values.append(phone_number)
    if email:
        fields.append("email = %s")
        values.append(email)
    if address:
        fields.append("address = %s")
        values.append(address)
    values.append(contact_name)
    query += ", ".join(fields) + " WHERE contact_name = %s"
    cursor.execute(query, values)
    connection.commit()


def delete_contact(connection, contact_name):
    cursor = connection.cursor()
    query = "DELETE FROM contacts WHERE contact_name = %s"
    cursor.execute(query, (contact_name,))
    connection.commit()


def main():
    connection = create_connection()
    if connection:
        while True:
            print("\nContact Management System")
            print("1. Add Contact")
            print("2. View Contacts")
            print("3. Search Contact")
            print("4. Update Contact")
            print("5. Delete Contact")
            print("6. Exit")
            choice = input("Enter your choice: ")
            
            if choice == '1':
                contact_name = input("Enter contact name: ")
                phone_number = input("Enter phone number: ")
                email = input("Enter email: ")
                address = input("Enter address: ")
                contact = Contact(contact_name, phone_number, email, address)
                add_contact(connection, contact)
            elif choice == '2':
                view_contacts(connection)
            elif choice == '3':
                search_term = input("Enter name or phone number to search: ")
                search_contact(connection, search_term)
            elif choice == '4':
                contact_name = input("Enter contact name to update: ")
                phone_number = input("Enter new phone number (leave blank to skip): ")
                email = input("Enter new email (leave blank to skip): ")
                address = input("Enter new address (leave blank to skip): ")
                update_contact(connection, contact_name, phone_number, email, address)
            elif choice == '5':
                contact_name = input("Enter contact name to delete: ")
                delete_contact(connection, contact_name)
            elif choice == '6':
                connection.close()
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
