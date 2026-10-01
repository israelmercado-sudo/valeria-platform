from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.api.tipificar import router_tipificar

app = FastAPI(
    title="Valeria Platform",
    description="IA especializada en Derecho Administrativo Peruano y Procedimientos Administrativos Disciplinarios",
    version="0.0.8"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def inicio():
    return {
        "nombre": "Valeria Platform",
        "estado": "online",
        "version": "0.0.8",
        "mensaje": "Analiza, fundamenta y redacta con precisión."
    }

app.include_router(router)
app.include_router(router_tipificar)