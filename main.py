import json
import time
import random
from typing import List, Dict


def add_book(title: str, author: str, year: str, status: str = "в наличии") -> None:
    valid_year = False
    while not valid_year:
        if not year.isdigit() or int(year) > 2024:
            print("Ошибка: Год должен быть числом и не может быть больше 2024. Пожалуйста, "
                  "введите корректный год.")
            year = input("Введите год: ")
        else:
            valid_year = True

    year = int(year)  # Преобразовываем год в число только после всех проверок

    # Проверяем, что статус соответствует одному из двух допустимых значений
    if status not in ["в наличии", "выдана"]:
        print("Ошибка: Статус должен быть 'в наличии' или 'выдана'. Установлено значение "
              "по умолчанию 'в наличии'.")
        status = "в наличии"

    book_id: str = generate_unique_id()

    new_book: Dict[str, str] = {
        "id": book_id,
        "title": title,
        "author": author,
        "year": year,
        "status": status
    }

    books_data: List[Dict[str, str]] = load_books_data()
    books_data.append(new_book)

    save_books_data(books_data)
    print("Книга успешно добавлена.")


def delete_book(book_id: str) -> None:
    books_data = load_books_data()
    updated_books_data = [book for book in books_data if book['id'] != book_id]

    if len(updated_books_data) < len(books_data):
        save_books_data(updated_books_data)
        print(f"Книга с ID {book_id} успешно удалена.")
    else:
        print(f"Книга с ID {book_id} не найдена.")


def search_book(query: str) -> None:
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
                f"ID: {found_book['id']}, Название: {found_book['title']},"
                f"Автор: {found_book['author']}, Год: {found_book['year']}, Статус: {found_book['status']}")
    else:
        print("Книги по запросу не найдены.")


def display_all_books() -> None:
    books_data = load_books_data()

    if books_data:
        print("Список всех книг:")
        for book in books_data:
            print(
                f"ID: {book['id']}, Название: {book['title']},"
                f"Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")
    else:
        print("Нет книг для отображения.")


def change_book_status(book_id: str, new_status: str) -> None:
    if new_status not in ["в наличии", "выдана"]:
        print("Ошибка: Статус должен быть 'в наличии' или 'выдана'.")
        return

    books_data = load_books_data()

    for book in books_data:
        if book['id'] == book_id:
            book['status'] = new_status
            save_books_data(books_data)
            print(f"Статус книги с ID {book_id} успешно изменен на {new_status}.")
            return

    print(f"Книга с ID {book_id} не найдена.")


def generate_unique_id() -> str:
    timestamp = int(time.time() * 1000)  # текущее время в миллисекундах
    random_number = random.randint(0, 1000)  # случайное число от 0 до 1000
    unique_id = f"{timestamp}-{random_number}"
    print(unique_id)
    return unique_id


def load_books_data() -> list:
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


def save_books_data(data: list) -> None:
    with open('books_data.json', 'w') as file:
        json.dump(data, file, indent=4)
