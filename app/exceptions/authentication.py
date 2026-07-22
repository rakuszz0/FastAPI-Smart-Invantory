class AuthenticationException(Exception):
    """
    Base Authentication Exception
    """

    def __init__(
        self,
        message: str = "Authentication Error"
    ):

        self.message = message

        super().__init__(self.message)


class InvalidCredentialException(
    AuthenticationException
):

    def __init__(
        self,
        message: str = "Invalid email or password"
    ):

        super().__init__(message)


class UserAlreadyExistsException(
    AuthenticationException
):

    def __init__(
        self,
        message: str = "User already exists"
    ):

        super().__init__(message)


class UnauthorizedException(
    AuthenticationException
):

    def __init__(
        self,
        message: str = "Unauthorized"
    ):

        super().__init__(message)


class ForbiddenException(
    AuthenticationException
):

    def __init__(
        self,
        message: str = "Forbidden"
    ):

        super().__init__(message)


class TokenExpiredException(
    AuthenticationException
):

    def __init__(
        self,
        message: str = "Token has expired"
    ):

        super().__init__(message)


class InvalidTokenException(
    AuthenticationException
):

    def __init__(
        self,
        message: str = "Invalid token"
    ):

        super().__init__(message)