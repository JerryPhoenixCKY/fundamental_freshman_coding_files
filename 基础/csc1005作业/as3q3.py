class Book:
    def __init__(self, isbn, title, author):
        self.__isbn = isbn
        self.__title = title
        self.__author = author
        self.__is_available = True
    def get_isbn(self):
        return self.__isbn
    def get_title(self):
        return self.__title
    def is_available(self):
        return self.__is_available
    def check_out(self):
        self.__is_available = False

    def return_book(self):
        self.__is_available = True


class Member:

    def __init__(self, member_id,name):
        self.__member_id = member_id
        self.__name = name
        self.__borrowed_books = []
    def get_member_id(self):
        return self.__member_id
    def get_borrowed_books(self):
        return self.__borrowed_books
    def borrow_book(self, book):
        if len(self.__borrowed_books) >= 3:
            print(f"Member {self.__member_id} has reached the maximum limit of 3 borrowed books.")
            exit()
        if book in self.__borrowed_books:
            print (f"Member {self.__member_id} already has this book.")
            exit()
        self.__borrowed_books.append(book)

    def return_book(self, book):

        if book not in self.__borrowed_books:
            print(f"Member {self.__member_id} does not have this book.")
            exit()
        self.__borrowed_books.remove(book)


class Library:
    def __init__(self):
        self.__books = []
        self.__members = []
    def add_book(self, book):
        if not isinstance(book, Book):
            print("Only Book objects can be added to the library.")
            exit()

        if any(i.get_isbn() == book.get_isbn() for i in self.__books):
            print(f"Book with ISBN {book.get_isbn()} already exists in the library.")

        self.__books.append(book)

    def add_member(self, member):

        if not isinstance(member, Member):
            print("Only Member objects can be added to the library.")
            exit()
        if any(i.get_member_id() == member.get_member_id() for i in self.__members):
            print(f"Member with ID {member.get_member_id()} already exists in the library.")
            exit()
        self.__members.append(member)

    def check_out_book(self, isbn, member_id):

        if not isinstance(isbn, str):
            print("ISBN must be a string.")
            exit()

        if not isinstance(member_id, str):
            print("Member ID must be a string.")
            exit()

        book = None
        for i in self.__books:
            if i.get_isbn() == isbn:
                book = i
                break

        if book is None:
            print(f"Book with ISBN {isbn} not found in the library.")
            exit()

        member=None
        for m in self.__members:
            if m.get_member_id() == member_id:
                member = m
                break

        if member is None:
            print(f"Member with ID {member_id} not found in the library.")
            exit()

        if not book.is_available():
            print(f"Book '{book.get_title()}' is currently unavailable.")
            exit()

        if len(member.get_borrowed_books()) >= 3:
            print(f"Member {member_id} has reached the maximum limit of 3 borrowed books.")
            exit()

        book.check_out()
        member.borrow_book(book)

    def return_book(self, isbn, member_id):

        if not isinstance(isbn, str) or not isbn.strip():
            print("ISBN must be a non-empty string.")
            exit()

        if not isinstance(member_id, str) or not member_id.strip():
            print("Member ID must be a non-empty string.")
            exit()

        book = None
        for i in self.__books:
            if i.get_isbn() == isbn:
                book = i
                break

        if book is None:
            print(f"Book with ISBN {isbn} not found in the library.")
            exit()

        member = None
        for m in self.__members:
            if m.get_member_id() == member_id:
                member = m
                break

        if member is None:
            print(f"Member with ID {member_id} not found in the library.")
            exit()

        if book not in member.get_borrowed_books():
           print(f"Member {member_id} does not have the book '{book.get_title()}' to return.")
           exit()
        book.return_book()
        member.return_book(book)

    def get_available_books(self):

        return [book for book in self.__books if book.is_available()]

    def get_member_books(self, member_id):

        if not isinstance(member_id, str):
            print("Member ID must be a string.")
            exit()

        member = None
        for m in self.__members:
            if m.get_member_id() == member_id:
                member = m
                break

        if member is None:
            print(f"Member with ID {member_id} not found in the library.")
            exit()

        return member.get_borrowed_books()

##############################################################

library = Library()


book1 = Book("123-456", "Python Programming", "John Smith")
book2 = Book("789-012", "Data Structures", "Jane Doe")
library.add_book(book1)
library.add_book(book2)

member = Member("M001", "Alice Brown")
library.add_member(member)

library.check_out_book("123-456", "M001")
