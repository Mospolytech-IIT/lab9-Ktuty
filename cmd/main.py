from db import engine, metadata_obj
import uvicorn
from fastapi import FastAPI

from handlers.post.router import post_router
from handlers.user.router import user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
