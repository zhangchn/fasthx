from collections.abc import Mapping
from typing import TYPE_CHECKING, Annotated, Any, Optional

import sys
if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias
from fastapi import Depends, Header
from fastapi import Request as FARequest

if TYPE_CHECKING:
    Request: TypeAlias = FARequest
else:
    Request: TypeAlias = Mapping[str, Any]
    """
    Alias for `Request` arguments.

    Workaround for this FastAPI bug: https://github.com/fastapi/fastapi/discussions/12403.
    And here's a FastAPI bugfix: https://github.com/fastapi/fastapi/pull/12406.

    This workaround should be removed when FastAPI had several new releases with the fix.
    """


def get_hx_request(
    request: FARequest, hx_request: Annotated[Optional[str], Header()] = None
) -> Optional[Request]:
    """
    FastAPI dependency that returns the current request if it is an HTMX one,
    i.e. it contains an `"HX-Request: true"` header.
    """
    return request if hx_request == "true" else None


def get_page_request(request: FARequest) -> Request:
    """
    Replacement dependency for `Request` to work around this FastAPI bug:
    https://github.com/fastapi/fastapi/discussions/12403.
    """
    return request


DependsHXRequest = Annotated[Optional[Request], Depends(get_hx_request)]
"""Annotated type (dependency) for `get_hx_request()` for FastAPI."""

DependsPageRequest = Annotated[Request, Depends(get_page_request)]
"""
Annotated `Request` dependency alias.

Workaround for this FastAPI bug: https://github.com/fastapi/fastapi/discussions/12403
"""
