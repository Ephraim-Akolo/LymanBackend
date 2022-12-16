from fastapi import FastAPI
from app.database import engine, Base
from .routers import artistans, customers, products, auth

Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
def root():
    return {'message': "Application Running"}

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(artistans.router)
app.include_router(products.router)

