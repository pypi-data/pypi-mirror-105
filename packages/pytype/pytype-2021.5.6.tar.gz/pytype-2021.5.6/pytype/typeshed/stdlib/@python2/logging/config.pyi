from _typeshed import AnyPath, StrPath
from threading import Thread
from typing import IO, Any, Callable, Dict, Optional, Union

from ConfigParser import RawConfigParser

_Path = StrPath

def dictConfig(config: Dict[str, Any]) -> None: ...
def fileConfig(
    fname: Union[str, IO[str]], defaults: Optional[Dict[str, str]] = ..., disable_existing_loggers: bool = ...
) -> None: ...
def listen(port: int = ...) -> Thread: ...
def stopListening() -> None: ...
