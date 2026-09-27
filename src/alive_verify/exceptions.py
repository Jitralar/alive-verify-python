class AliveVerifyError(Exception):
    """Base exception for the Alive Verify client."""


class AliveAPIError(AliveVerifyError):
    """Error returned by the Alive Verify API."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response: dict | None = None,
    ):
        super().__init__(message)

        self.message = message
        self.status_code = status_code
        self.response = response


class AliveAuthenticationError(AliveAPIError):
    """Authentication failed."""


class AliveForbiddenError(AliveAPIError):
    """The account is not allowed to perform the requested operation."""


class AliveValidationError(AliveAPIError):
    """The API rejected request parameters."""