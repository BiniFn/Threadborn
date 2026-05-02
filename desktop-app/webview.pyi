# Type stubs for pywebview (imported as `webview`)
from typing import Any

def create_window(
    title: str,
    url: str = ...,
    *,
    width: int = ...,
    height: int = ...,
    min_size: tuple[int, int] = ...,
    text_select: bool = ...,
    **kwargs: Any,
) -> Any: ...
def start(*args: Any, **kwargs: Any) -> None: ...
