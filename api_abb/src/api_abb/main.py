from fastapi import FastAPI
from api_abb.api.children import router as children_router

app = FastAPI(
    title="API ABB - Gestión de Niños",
    description="API REST para gestionar registros de niños usando un Árbol Binario de Búsqueda (ABB)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(children_router)


@app.get("/", tags=["root"])
def root():
    """Endpoint raíz de la API."""
    return {
        "message": "API ABB - Gestión de Niños",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["health"])
def health_check():
    """Verificar el estado de la API."""
    return {"status": "healthy"}
