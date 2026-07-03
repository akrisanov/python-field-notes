"""
Showing analogy to asyncio.ensure_future().
This is a utility function to make life easier for framework developers,
not end-user developers like you and I.
"""

from typing import Any, List


def listify(x: Any) -> List:
    """A utility function for coercing input into a list."""
    if isinstance(x, (str, bytes)):
        return [x]
    try:
        return [_ for _ in x]
    except TypeError:
        return [x]
