from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    """..."""
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BodyRequest(BaseModel):
    """Validate book attributes"""
    id: Optional[int] = Field(
        description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(ge=1999, le=datetime.now().year)


# List of book objects
BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby',
         'A very nice book', 5, 2021),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book', 5, 2013),
    Book(3, 'Master Endpoints', 'codingwithroby', 'An awesome book', 5, 2020),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2021),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 1999),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2005)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    """Read and return list of
    all books"""
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):  # Add validation for Path Param
    """Read book given the book id"""
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


@app.get("/books/", status_code=status.HTTP_200_OK)
# Add validation for Query Param
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    """Read books with the passed rating"""
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
# Add validation for Query Param
async def read_books_by_publish_date(published_date: int = Query(ge=1999, le=datetime.now().year)):
    """Read books with the published date"""
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(body_request: BodyRequest):
    """ Adds a new book to the catalogue of books """
    new_book = Book(**body_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    """Finds the book ID of the recently added book,
    and assigns the new book and appropriate ID"""
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BodyRequest):
    """Update an existing book given the book
    title"""
    book_changed = False
    for index, book in enumerate(BOOKS):
        if book.title.casefold() == book_request.title.casefold():
            BOOKS[index] = Book(**book_request.model_dump())
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
# Add validation for Path Parameter
async def delete_book(book_id: int = Path(gt=0)):
    """Delete book from catalogue given it's book ID"""
    book_deleted = False
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(index)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item not found')
