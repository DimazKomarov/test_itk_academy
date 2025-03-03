import uvicorn

from fastapi import FastAPI

from api.endpoints.currency import router as currency_router
from api.endpoints.users import router as users_router


app = FastAPI()
app.include_router(currency_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
