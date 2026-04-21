import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tren import router as router_tren
from auth import router as router_auth

app = FastAPI()

app.include_router(router_tren)
app.include_router(router_auth)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5501", 
        "http://127.0.0.1:5501",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ], 
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)