from fastapi import Request

from punq import Container


def get_registry(request: Request) -> Container:
    """
    Returns a registry with all initialized dependencies.

    @param request:
        The incoming request that contains a registry.
    @return:
        The registry.
    """
    return request.state.registry
