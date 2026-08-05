from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .router_global import api_router


app = FastAPI(
    title='Api modular COEXCA03',
    description='API para el centro de conservación de carreteras de CA-35 y CA-36',
    version='1.0.0'
)

app.add_middleware(
    CORSMidleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix="/api/v1")

Base.metadata.create_all(bind=engine)