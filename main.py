import json
import time
import random


def add_book(title, author, year):
    book_id = generate_unique_id()
    status = "в наличии"

    new_book = {
        "id": book_id,
        "title": title,
        "author": author,
        "year": year,
        "status": status
    }

    books_data = load_books_data()
    books_data.append(new_book)

    save_books_data(books_data)
    print("Книга успешно добавлена.")


def delete_book(book_id):
    books_data = load_books_data()
    updated_books_data = [book for book in books_data if book['id'] != book_id]

    if len(updated_books_data) < len(books_data):
        save_books_data(updated_books_data)
        print(f"Книга с ID {book_id} успешно удалена.")
    else:
        print(f"Книга с ID {book_id} не найдена.")


def search_book(query):
    books_data = load_books_data()

    found_books = []
    for book in books_data:
        if query.lower() in book['title'].lower() or query.lower() in book['author'].lower() or query == str(
                book['year']):
            found_books.append(book)

    if found_books:
        print("Найденные книги:")
        for found_book in found_books:
            print(
                f"ID: {found_book['id']}, Название: {found_book['title']}, Автор: {found_book['author']}, Год: {found_book['year']}, Статус: {found_book['status']}")
    else:
        print("Книги по запросу не найдены.")


def display_all_books():
    books_data = load_books_data()

    if books_data:
        print("Список всех книг:")
        for book in books_data:
            print(
                f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")
    else:
        print("Нет книг для отображения.")


def change_book_status(book_id, new_status):
    books_data = load_books_data()

    for book in books_data:
        if book['id'] == book_id:
            book['status'] = new_status
            save_books_data(books_data)
            print(f"Статус книги с ID {book_id} успешно изменен на {new_status}.")
            return

    print(f"Книга с ID {book_id} не найдена.")


def generate_unique_id():
    timestamp = int(time.time() * 1000)  # текущее время в миллисекундах
    random_number = random.randint(0, 1000)  # случайное число от 0 до 1000
    unique_id = f"{timestamp}-{random_number}"
    print(unique_id)
    return unique_id


def load_books_data():
    try:
        with open('books_data.json', 'r') as file:
            data = file.read()
            if not data:
                return []
            return json.loads(data)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # Если файл не существует или содержит некорректные данные JSON
        initial_data = []  # Здесь определяются изначальные данные
        save_books_data(initial_data)  # Сохраняем изначальные данные в файл
        return initial_data


def save_books_data(data):
    with open('books_data.json', 'w') as file:
        json.dump(data, file, indent=4)
