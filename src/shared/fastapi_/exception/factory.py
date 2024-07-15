from fastapi import HTTPException
from fastapi import status

from shared.exception.base import BaseAppException
from shared.exception.forbidden import Forbidden
from shared.exception.no_authorized import NotAuthorized
from shared.exception.not_found import NotFound


def exception_factory(exc: BaseAppException) -> HTTPException:
    """
    Returns a specific `HTTPException` based on `exc` parameter.

    @param exc:
        The exception that must be converted to the HTTP exception.
    @return:
        The `HTTPException` instance with the appropriate message and status code.
    """
    match exc:
        case NotFound():
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            )
        case Forbidden():
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(exc),
            )
        case NotAuthorized():
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(exc),
            )

    raise ValueError(f"{type(exc)} can't be handled as an HTTPException.")
