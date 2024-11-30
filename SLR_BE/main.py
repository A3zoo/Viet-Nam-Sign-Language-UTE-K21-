from fastapi import FastAPI
import os
from api.routes import router as api_router
from api.slr import router as slr_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from model.dto.TestDTO import TestDTO



load_dotenv()
HOST = os.getenv("SLR_HOST", "127.0.0.1") 
PORT = int(os.getenv("SLR_PORT", 8000)) 
middleware_url = os.getenv("SLR_ALLOW_URL", "http://localhost:3000")

app = FastAPI(title='SLR', version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=middleware_url, 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
    
@app.post("/test")
async def test(payload: TestDTO):
    return {"age": payload.age, "name": payload.name}

@app.get('/')
async def home():
    return "Home"

app.include_router(api_router, prefix="/api/v1")
app.include_router(slr_router, prefix="/api/v1")

if __name__ == '__main__':
    uvicorn.run("main:app",host=HOST, port=PORT, reload=True)
