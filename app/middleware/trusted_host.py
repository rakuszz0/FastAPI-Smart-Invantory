from fastapi.middleware.trustedhost import TrustedHostMiddleware


def setup_trusted_host(app):

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "*.localhost",
            "*.mycompany.com",
            "testserver",
        ]
    )