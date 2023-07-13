from enum import Enum
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# path operations are evaluated in order
# 따라서 /users/me 를 /users/{user_id} 보다 먼저 선언해야 한다.


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}

# enum을 이용해서


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

# Defaults


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

# http://127.0.0.1:8000/items/
# http://127.0.0.1:8000/items/?skip=0&limit=10

# Optional parameters


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Multiple path and query parameters


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# request body
{
    "name": "abcd",
    "description": "i am abcd",
    "price": 1000,
    "tax": 10
}


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# same
# q: str | None = None
# q: Annotated[str | None] = None
# 차이점:
# - 메타 정보를 줄 수 있음, 아래 경우 쿼리 파라미터에서 값을 받고자 한다는 걸 알게 할 수 있다.
# - 50자 아래라는 validation도 할 수 있음
#   - 그래서 데이터가 유효하지 않을 때 더 명확한 에러를 보여줄 수 있음
# - docs에도 잘 표시됨


@app.get("/items/")
async def read_items(
        q: Annotated[
            str | None,
            Query(
                title="Query string",
                description="Query string for the items to search in the database that have a good match",
                min_length=3,
            ),
        ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
