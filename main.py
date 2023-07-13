from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()

# Query, Path 파라미터와 같은 방식으 쿠키 파라미터 정의 가능


@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
