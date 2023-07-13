from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()

# Query, Path 파라미터와 같은 방식으로 헤더 파라미터 정의 가능


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
