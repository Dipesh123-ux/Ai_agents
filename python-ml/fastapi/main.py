from fastapi import FastAPI, Header
from typing import Optional

app = FastAPI()


@app.get('/')
async def read_root():
    return {"message" : "Hello world"}

@app.get('/greet')
async def greet_name(name:Optional[str] = "dipesh",age : int = 0) -> dict:
    return {"message" : f"Hello {name}", "age" : age}
    
@app.get('/get_headers')
async def get_headers(accept : str = Header(None)):
    return {accept}