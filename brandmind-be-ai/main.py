from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.router import api_router
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get('/')
def root():
    """
    Root endpoint to test API availability.
    """
    return JSONResponse(
        'WELLCOME TO BRANDMIND AI'
    )

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(api_router, prefix="/api")


if __name__== "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)