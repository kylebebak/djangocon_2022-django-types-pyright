from __future__ import annotations

from typing import TypeVar


T = TypeVar("T")


def not_none(var: T | None) -> T:
    """
    Assert that var is not None and return var.

    This narrows type from `T | None` -> `T`.
    """
    assert var is not None
    return var
