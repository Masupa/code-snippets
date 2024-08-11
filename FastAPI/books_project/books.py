from fastapi import Body, FastAPI

app = FastAPI()  # Makes the file a FastAPI app

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Six', 'category': 'math'},
]


@app.get("/books")  # Static API -> Path or URL Path doesn't change
async def read_all_books():
    """ Returns all books """
    return BOOKS


@app.get("/books/{book_title}")  # Dynamic API -> Path or URL Path can change
async def read_book(book_title: str):
    """ Returns book given the book title """
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return None


# Anything passed in that is not a "dynamic parameters" will be converted into a query parameter
# E.g. "https://127.0.0.0.1:8000/books/?category=science"
@app.get("/books/")
async def read_category_by_query(category: str):
    """ Returns all books with the passed category """
    books_to_return = []
    for book in BOOKS:
        if book['category'].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    """ Returns all books written by the same author match
    the passed category """
    books_to_return = []
    for book in BOOKS:
        if book['author'].casefold() == book_author.casefold() and \
                book['category'].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# Post methods have a body; get methods can't have a body
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    """Add a new book"""
    BOOKS.append(new_book)
