from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    """..."""
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BodyRequest(BaseModel):
    """Validate book attributes"""
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)

# List of book objects
BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book', 5),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book', 5),
    Book(3, 'Master Endpoints', 'codingwithroby', 'An awesome book', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]

@app.get("/books")
async def read_all_books():
    """Read and return list of
    all books"""
    return BOOKS

@app.post("/create-book")
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
