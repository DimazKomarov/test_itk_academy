import uvicorn

from fastapi import FastAPI

from api.endpoints.wallets import router as wallets_router
from api.endpoints.users import router as users_router


app = FastAPI()
app.include_router(wallets_router)
app.include_router(users_router)

@app.get("/")
def index():
    return {"message": "Добро пожаловать!"}


# if __name__ == "__main__":
#     uvicorn.run(app="main:app", reload=True)
