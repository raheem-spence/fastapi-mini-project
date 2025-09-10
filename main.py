from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Book(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_books = [{"title": "title of book 1", "content": "content of book 1", "id": 1}, 
            {"title": "favorite books", "content": "I like Harry Potter", "id": 2}]

def find_book(id):
    for b in my_books:
        if b["id"] == id:
            return b
        
def find_index_book(id):
    for i, b in enumerate(my_books):
        if b['id'] == id:
            return i


@app.get("/")
def say_hello():
    return {"message": "Hello World"}

# Get all books (R)
@app.get("/books")
def get_books():
    return {"data": my_books}

# Create book (C)
@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_books(book: Book):
    book_dict = book.model_dump()
    book_dict['id'] = randrange(0, 1000000)
    my_books.append(book_dict)
    return {"data": book_dict}

# Get individual book (R)
@app.get("/books/{id}")
def get_book(id: int, response: Response):
    book = find_book(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"book with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"messsage": f"book with id: {id} was not found"}
    return {"book_detail": book}

# Delete a book (D)
@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int):
    # deleting post
    # find index in the list that has required ID
    # my_books.pop(pop)
    index = find_index_book(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    my_books.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a book (U)
@app.put("/books/{id}")
def update_book(id: int, book: Book):
    index = find_index_book(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    book_dict = book.model_dump()
    book_dict['id'] = id
    my_books[index] = book_dict
    return {"data": book_dict}