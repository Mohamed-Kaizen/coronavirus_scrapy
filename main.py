from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="corona virus real time data",
    description="",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
