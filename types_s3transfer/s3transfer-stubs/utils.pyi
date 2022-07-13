from typing import IO, Any, Callable, Dict, Iterable, List, Optional, Sequence

from _typeshed import Incomplete
from botocore.awsrequest import AWSRequest
from s3transfer.compat import SOCKET_ERROR as SOCKET_ERROR
from s3transfer.compat import fallocate as fallocate
from s3transfer.compat import rename_file as rename_file
from s3transfer.futures import TransferFuture

MAX_PARTS: int
MAX_SINGLE_UPLOAD_SIZE: Incomplete
MIN_UPLOAD_CHUNKSIZE: Incomplete
logger: Incomplete
S3_RETRYABLE_DOWNLOAD_ERRORS: Incomplete

def random_file_extension(num_digits: int = ...) -> str: ...
def signal_not_transferring(request: AWSRequest, operation_name: str, **kwargs: Any) -> None: ...
def signal_transferring(request: AWSRequest, operation_name: str, **kwargs: Any) -> None: ...
def calculate_num_parts(size: int, part_size: int) -> int: ...
def calculate_range_parameter(
    part_size: int, part_index: int, num_parts: int, total_size: Optional[int] = ...
) -> str: ...
def get_callbacks(
    transfer_future: TransferFuture, callback_type: str
) -> List[Callable[..., Any]]: ...
def invoke_progress_callbacks(
    callbacks: Iterable[Callable[..., Any]], bytes_transferred: int
) -> None: ...
def get_filtered_dict(
    original_dict: Dict[str, Any], whitelisted_keys: Sequence[str]
) -> Dict[str, Any]: ...

class CallArgs:
    def __init__(self, **kwargs: Any) -> None: ...

class FunctionContainer:
    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None: ...
    def __call__(self) -> Any: ...

class CountCallbackInvoker:
    def __init__(self, callback: Callable[..., Any]) -> None: ...
    @property
    def current_count(self) -> int: ...
    def increment(self) -> None: ...
    def decrement(self) -> None: ...
    def finalize(self) -> None: ...

class OSUtils:
    def get_file_size(self, filename: str) -> int: ...
    def open_file_chunk_reader(
        self, filename: str, start_byte: int, size: int, callbacks: Iterable[Callable[..., Any]]
    ) -> ReadFileChunk: ...
    def open_file_chunk_reader_from_fileobj(
        self,
        fileobj: IO[Any],
        chunk_size: int,
        full_file_size: int,
        callbacks: Iterable[Callable[..., Any]],
        close_callbacks: Incomplete | None = ...,
    ) -> ReadFileChunk: ...
    def open(self, filename: str, mode: str) -> IO[Any]: ...
    def remove_file(self, filename: str) -> None: ...
    def rename_file(self, current_filename: str, new_filename: str) -> None: ...
    def is_special_file(cls, filename: str) -> bool: ...
    def get_temp_filename(self, filename: str) -> str: ...
    def allocate(self, filename: str, size: int) -> None: ...

class DeferredOpenFile:
    def __init__(
        self, filename, start_byte: int = ..., mode: str = ..., open_function=...
    ) -> None: ...
    @property
    def name(self): ...
    def read(self, amount: Incomplete | None = ...): ...
    def write(self, data) -> None: ...
    def seek(self, where, whence: int = ...) -> None: ...
    def tell(self): ...
    def close(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, *args, **kwargs) -> None: ...

class ReadFileChunk:
    def __init__(
        self,
        fileobj,
        chunk_size,
        full_file_size,
        callbacks: Incomplete | None = ...,
        enable_callbacks: bool = ...,
        close_callbacks: Incomplete | None = ...,
    ) -> None: ...
    @classmethod
    def from_filename(
        cls,
        filename,
        start_byte,
        chunk_size,
        callbacks: Incomplete | None = ...,
        enable_callbacks: bool = ...,
    ): ...
    def read(self, amount: Incomplete | None = ...): ...
    def signal_transferring(self) -> None: ...
    def signal_not_transferring(self) -> None: ...
    def enable_callback(self) -> None: ...
    def disable_callback(self) -> None: ...
    def seek(self, where, whence: int = ...) -> None: ...
    def close(self) -> None: ...
    def tell(self): ...
    def __len__(self): ...
    def __enter__(self): ...
    def __exit__(self, *args, **kwargs) -> None: ...
    def __iter__(self): ...

class StreamReaderProgress:
    def __init__(self, stream, callbacks: Incomplete | None = ...) -> None: ...
    def read(self, *args, **kwargs): ...

class NoResourcesAvailable(Exception): ...

class TaskSemaphore:
    def __init__(self, count) -> None: ...
    def acquire(self, tag, blocking: bool = ...) -> None: ...
    def release(self, tag, acquire_token) -> None: ...

class SlidingWindowSemaphore(TaskSemaphore):
    def __init__(self, count) -> None: ...
    def current_count(self): ...
    def acquire(self, tag, blocking: bool = ...): ...
    def release(self, tag, acquire_token) -> None: ...

class ChunksizeAdjuster:
    max_size: Incomplete
    min_size: Incomplete
    max_parts: Incomplete
    def __init__(self, max_size=..., min_size=..., max_parts=...) -> None: ...
    def adjust_chunksize(self, current_chunksize, file_size: Incomplete | None = ...): ...