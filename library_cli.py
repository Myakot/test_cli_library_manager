import argparse
from main import add_book, delete_book, search_book, display_all_books, change_book_status


def main() -> None:
    parser = argparse.ArgumentParser(description="Library Management CLI")
    parser.add_argument("--add", nargs=3, help="Add a new book: title author year")
    parser.add_argument("--delete", type=str, help="Delete a book by ID")
    parser.add_argument("--search", help="Search for a book by title, author, or year")
    parser.add_argument("--display", action="store_true", help="Display all books")
    parser.add_argument("--change-status", nargs=2, help="Change the status of a book by ID: new_status")

    args = parser.parse_args()

    if args.add:
        title, author, year = args.add
        add_book(title, author, int(year))
    elif args.delete:
        delete_book(args.delete)
    elif args.search:
        search_book(args.search)
    elif args.display:
        display_all_books()
    elif args.change_status:
        book_id, new_status = args.change_status[0], args.change_status[1]
        # Получить идентификатор книги и новый статус из списка
        change_book_status(book_id, new_status)
    else:
        print("Please provide a valid command.")


if __name__ == "__main__":
    main()
