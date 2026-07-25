from fastapi import FastAPI

# Routers
from app.routers.product_router import router as product_router
from app.routers.supplier_router import router as supplier_router
from app.routers.auth_router import router as auth_router
from app.routers.customer_router import router as customer_router
from app.routers.transaction_router import router as transaction_router
from app.routers.ai_router import router as ai_router
from app.routers.admin_router import router as admin_router
from app.routers.payment_router import router as payment_router
from app.routers.profile_router import router as profile_router

# Dependencies
from app.dependencies.services import get_product_service
from app.dependencies.services import get_supplier_service

# Middleware
from app.middleware.cors import setup_cors
from app.middleware.trusted_host import setup_trusted_host
from app.middleware.logging import LoggingMiddleware
from app.middleware.timer import TimerMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.rate_limit import RateLimitMiddleware

# Exception
from app.exceptions.handlers import register_exception_handlers


app = FastAPI(
    title="Smart Inventory API",
    description="Inventory Management System with AI Recommendation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# =====================================
# Middleware
# =====================================

setup_cors(app)
setup_trusted_host(app)

app.add_middleware(LoggingMiddleware)
app.add_middleware(TimerMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)

# =====================================
# Exception Handler
# =====================================

register_exception_handlers(app)

# =====================================
# API Version
# =====================================

API_PREFIX = "/api/v1"

# =====================================
# Router
# =====================================

app.include_router(
    product_router,
    prefix=API_PREFIX
)

app.include_router(
    supplier_router,
    prefix=API_PREFIX
)

app.include_router(
    auth_router,
    prefix=API_PREFIX
)

app.include_router(
    profile_router,
    prefix=API_PREFIX
)

app.include_router(
    customer_router,
    prefix=API_PREFIX
)

app.include_router(
    transaction_router,
    prefix=API_PREFIX
)

app.include_router(
    ai_router,
    prefix=API_PREFIX
)

app.include_router(
    admin_router,
    prefix=API_PREFIX
)

app.include_router(
    payment_router,
    prefix=API_PREFIX
)

# Nanti tinggal aktifkan
#
# app.include_router(customer_router, prefix=API_PREFIX)
# app.include_router(transaction_router, prefix=API_PREFIX)
# app.include_router(auth_router, prefix=API_PREFIX)
# app.include_router(ai_router, prefix=API_PREFIX)

# =====================================
# Root
# =====================================

@app.get("/", tags=["Root"])
def root():

    return {
        "success": True,
        "message": "Smart Inventory API Running 🚀",
        "version": "1.0.0"
    }


# =====================================
# Health Check
# =====================================

@app.get("/health", tags=["Health"])
def health():

    return {
        "status": "healthy"
    }
