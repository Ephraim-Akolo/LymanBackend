import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import artistans, customers, products, auth

# Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#["https://www.google.com", "https://www.youtube.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
def root():
    return {'message': "Application Running"}

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(artistans.router)
app.include_router(products.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
