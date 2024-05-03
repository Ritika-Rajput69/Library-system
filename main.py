import json

class Book:
    total_books = 0

    def __init__(self, title, author, is_issued=False, issued_to=None):
        Book.total_books += 1
        self.book_id = Book.total_books
        self.title = title
        self.author = author
        self.is_issued = is_issued
        self.issued_to = issued_to

    def __str__(self):
        return f"Book ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Issued: {self.is_issued}, Issued To: {self.issued_to}"

class Library:
    def __init__(self, books_file):
        self.books_file = books_file
        self.books = self.load_books()

    def load_books(self):
        try:
            with open(self.books_file, 'r') as file:
                books_data = json.load(file)
                books = []
                for book_data in books_data:
                    book = Book(book_data['title'], book_data['author'], book_data['is_issued'], book_data['issued_to'])
                    books.append(book)
                Book.total_books = len(books)
                return books
        except FileNotFoundError:
            return []

    def save_books(self):
        books_data = [{'book_id': book.book_id, 'title': book.title, 'author': book.author,
                       'is_issued': book.is_issued, 'issued_to': book.issued_to} for book in self.books]
        with open(self.books_file, 'w') as file:
            json.dump(books_data, file, indent=4)

    def display_all_books(self):
        if self.books:
            print("All Books in the Library:")
            for book in self.books:
                print(book)
        else:
            print("No books in the library.")

    def add_book(self, book):
        self.books.append(book)
        self.save_books()
        print("Book added successfully.")

    def issue_book(self, book_id, student_name):
        for book in self.books:
            if book.book_id == book_id and not book.is_issued:
                book.is_issued = True
                book.issued_to = student_name
                self.save_books()
                print(f"Book '{book.title}' issued successfully to {student_name}.")
                return
        print("Book is either already issued or not available.")

    def return_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id and book.is_issued:
                book.is_issued = False
                book.issued_to = None
                self.save_books()
                print(f"Book '{book.title}' has been returned.")
                return
        print("Book is not currently issued or not available.")

    def display_issued_books(self):
        issued_books = [book for book in self.books if book.is_issued]
        if issued_books:
            print("Issued Books:")
            for book in issued_books:
                print(book)
        else:
            print("No books are currently issued.")

# Create library object with books file
library = Library('books.json')

while True:
    print("\n--- Library Management System ---")
    print("1. Display all books")
    print("2. Add a book")
    print("3. Issue a book")
    print("4. Return a book")
    print("5. Display issued books")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        library.display_all_books()
    elif choice == '2':
        title = input("Enter title: ")
        author = input("Enter author: ")
        new_book = Book(title, author)
        library.add_book(new_book)
    elif choice == '3':
        book_id = int(input("Enter book ID to issue: "))
        student_name = input("Enter student name: ")
        library.issue_book(book_id, student_name)
    elif choice == '4':
        book_id = int(input("Enter book ID to return: "))
        library.return_book(book_id)
    elif choice == '5':
        library.display_issued_books()
    elif choice == '6':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please choose again.")
