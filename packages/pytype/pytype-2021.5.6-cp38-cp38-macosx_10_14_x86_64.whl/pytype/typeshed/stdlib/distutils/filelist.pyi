from typing import Iterable, List, Optional, Pattern, Union, overload
from typing_extensions import Literal

# class is entirely undocumented
class FileList:
    allfiles: Optional[Iterable[str]] = ...
    files: List[str] = ...
    def __init__(self, warn: None = ..., debug_print: None = ...) -> None: ...
    def set_allfiles(self, allfiles: Iterable[str]) -> None: ...
    def findall(self, dir: str = ...) -> None: ...
    def debug_print(self, msg: str) -> None: ...
    def append(self, item: str) -> None: ...
    def extend(self, items: Iterable[str]) -> None: ...
    def sort(self) -> None: ...
    def remove_duplicates(self) -> None: ...
    def process_template_line(self, line: str) -> None: ...
    @overload
    def include_pattern(
        self, pattern: str, anchor: Union[int, bool] = ..., prefix: Optional[str] = ..., is_regex: Literal[0, False] = ...
    ) -> bool: ...
    @overload
    def include_pattern(self, pattern: Union[str, Pattern[str]], *, is_regex: Literal[True, 1] = ...) -> bool: ...
    @overload
    def include_pattern(
        self,
        pattern: Union[str, Pattern[str]],
        anchor: Union[int, bool] = ...,
        prefix: Optional[str] = ...,
        is_regex: Union[int, bool] = ...,
    ) -> bool: ...
    @overload
    def exclude_pattern(
        self, pattern: str, anchor: Union[int, bool] = ..., prefix: Optional[str] = ..., is_regex: Literal[0, False] = ...
    ) -> bool: ...
    @overload
    def exclude_pattern(self, pattern: Union[str, Pattern[str]], *, is_regex: Literal[True, 1] = ...) -> bool: ...
    @overload
    def exclude_pattern(
        self,
        pattern: Union[str, Pattern[str]],
        anchor: Union[int, bool] = ...,
        prefix: Optional[str] = ...,
        is_regex: Union[int, bool] = ...,
    ) -> bool: ...

def findall(dir: str = ...) -> List[str]: ...
def glob_to_re(pattern: str) -> str: ...
@overload
def translate_pattern(
    pattern: str, anchor: Union[int, bool] = ..., prefix: Optional[str] = ..., is_regex: Literal[False, 0] = ...
) -> Pattern[str]: ...
@overload
def translate_pattern(pattern: Union[str, Pattern[str]], *, is_regex: Literal[True, 1] = ...) -> Pattern[str]: ...
@overload
def translate_pattern(
    pattern: Union[str, Pattern[str]],
    anchor: Union[int, bool] = ...,
    prefix: Optional[str] = ...,
    is_regex: Union[int, bool] = ...,
) -> Pattern[str]: ...
