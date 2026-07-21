from fastapi import FastAPI

from app.routers.product_router import router as product_router
from app.routers.supplier_router import router as supplier_router

app = FastAPI(
    title="Sales AI API",
    version="1.0.0"
)

app.include_router(product_router)
app.include_router(supplier_router)


@app.get("/")
def root():
    return {
        "message": "Sales AI API Running 🚀"
    }