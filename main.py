import json
import time
import random
from typing import List, Dict


def add_book(title: str, author: str, year: str, status: str = "в наличии") -> None:
    """
    Добавляет новую книгу в библиотеку.

    Параметры:
    - title (str): Название книги.
    - author (str): Автор книги.
    - year (str): Год издания книги.
    - status (str, optional): Статус книги. Допустимые значения: "в наличии", "выдана". По умолчанию "в наличии".

    Выполняет проверку введенного года и статуса книги. Генерирует уникальный идентификатор для книги.
    Добавляет книгу в хранилище данных и выводит сообщение об успешном добавлении.
    """

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
    """
    Удаляет книгу из библиотеки по её ID.

    Параметры:
    - book_id (str): Уникальный идентификатор книги, которую необходимо удалить.

    Проверяет наличие книги в библиотеке. Если книга найдена, удаляет её и выводит сообщение об успешном удалении.
    В противном случае сообщает, что книга с таким ID не найдена.
    """

    books_data = load_books_data()
    updated_books_data = [book for book in books_data if book['id'] != book_id]

    if len(updated_books_data) < len(books_data):
        save_books_data(updated_books_data)
        print(f"Книга с ID {book_id} успешно удалена.")
    else:
        print(f"Книга с ID {book_id} не найдена.")


def search_book(query: str) -> None:
    """
    Ищет книги по заданному запросу.

    Параметры:
    - query (str): Поисковый запрос, который может быть названием, автором или годом издания книги.

    Отображает найденные книги, соответствующие запросу, или сообщает об отсутствии результатов.
    """

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
    """
    Отображает список всех книг в библиотеке.

    Для каждой книги отображает её ID, название, автора, год издания и статус.
    Если в библиотеке нет книг, выводит сообщение об этом.
    """

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
    """
    Изменяет статус книги на новый.

    Параметры:
    - book_id (str): Уникальный идентификатор книги.
    - new_status (str): Новый статус для книги. Допустимые значения: "в наличии", "выдана".

    Проверяет, соответствует ли новый статус одному из допустимых значений.
    Если да, изменяет статус книги и выводит соответствующее сообщение.
    В случае, если книга с указанным ID не найдена, выводит сообщение об этом.
    """

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
    """
    Генерирует уникальный идентификатор.

    Идентификатор формируется путём конкатенации текущего времени в миллисекундах и случайного числа в диапазоне от 0 до 1000.
    Это обеспечивает высокую вероятность уникальности идентификатора.

    Возвращает:
    - str: Строка, представляющая собой уникальный идентификатор.
    """

    timestamp = int(time.time() * 1000)  # текущее время в миллисекундах
    random_number = random.randint(0, 1000)  # случайное число от 0 до 1000
    unique_id = f"{timestamp}-{random_number}"
    print(unique_id)
    return unique_id


def load_books_data() -> list:
    """
    Загружает данные о книгах из хранилища.

    Возвращает список словарей, каждый из которых содержит информацию о книге.
    Если хранилище пусто, возвращает пустой список.
    """

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
    """
    Сохраняет обновлённые данные о книгах в хранилище.

    Параметры:
    - books_data (list): Список словарей с данными о книгах для сохранения.

    Перезаписывает хранилище данными из переданного списка, обновляя информацию о книгах.
    """

    with open('books_data.json', 'w') as file:
        json.dump(data, file, indent=4)
