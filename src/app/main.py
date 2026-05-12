from fastapi import FastAPI
import uvicorn

from api.v1.routes import router

app = FastAPI(
    title="Api для магазина",
    version="1.0.0",
    root_path=""
    )

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
