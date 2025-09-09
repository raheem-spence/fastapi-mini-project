from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/hello")
def say_hello():
    return {"message": "Hello World"}

@app.post("/item")
def create_book(payload: dict = Body(...)):
    print(payload)
    return {"message": f"Title of book is '{payload['name']}'"}