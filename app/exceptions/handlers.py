from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.product import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    ProductOutOfStockException,
)

from app.exceptions.supplier import (
    SupplierNotFoundException,
    SupplierAlreadyExistsException,
)

from app.exceptions.customer import (
    CustomerNotFoundException,
    CustomerAlreadyExistsException,
)

from app.exceptions.transaction import (
    TransactionNotFoundException,
    InvalidTransactionException,
)

from app.exceptions.authentication import (
    InvalidCredentialException,
    UserAlreadyExistsException,
    UnauthorizedException,
    ForbiddenException,
    TokenExpiredException,
    InvalidTokenException,
)

def register_exception_handlers(
    app: FastAPI,
):

    @app.exception_handler(ProductNotFoundException)
    async def product_not_found(
        request: Request,
        exc: ProductNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(ProductAlreadyExistsException)
    async def product_exists(
        request: Request,
        exc: ProductAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(ProductOutOfStockException)
    async def product_stock(
        request: Request,
        exc: ProductOutOfStockException,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(SupplierNotFoundException)
    async def supplier_not_found(
        request: Request,
        exc: SupplierNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(SupplierAlreadyExistsException)
    async def supplier_exists(
        request: Request,
        exc: SupplierAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(CustomerNotFoundException)
    async def customer_not_found(
        request: Request,
        exc: CustomerNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(CustomerAlreadyExistsException)
    async def customer_exists(
        request: Request,
        exc: CustomerAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(TransactionNotFoundException)
    async def transaction_not_found(
        request: Request,
        exc: TransactionNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(InvalidTransactionException)
    async def invalid_transaction(
        request: Request,
        exc: InvalidTransactionException,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message,
            },
        )
    

    @app.exception_handler(InvalidCredentialException)
    async def invalid_credential_handler(
        request: Request,
        exc: InvalidCredentialException,
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(UserAlreadyExistsException)
    async def user_exists_handler(
        request: Request,
        exc: UserAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(
        request: Request,
        exc: UnauthorizedException,
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(
        request: Request,
        exc: ForbiddenException,
    ):
        return JSONResponse(
            status_code=403,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(TokenExpiredException)
    async def token_expired_handler(
        request: Request,
        exc: TokenExpiredException,
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_handler(
        request: Request,
        exc: InvalidTokenException,
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": exc.message,
            },
        )