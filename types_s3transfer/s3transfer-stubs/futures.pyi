import logging
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Sequence, Type

from s3transfer.compat import MAXINT as MAXINT
from s3transfer.exceptions import TransferNotDoneError as TransferNotDoneError
from s3transfer.tasks import Task
from s3transfer.utils import FunctionContainer as FunctionContainer
from s3transfer.utils import TaskSemaphore as TaskSemaphore

logger: logging.Logger

class BaseTransferFuture:
    @property
    def meta(self) -> TransferMeta: ...
    def done(self) -> bool: ...
    def result(self) -> None: ...
    def cancel(self) -> None: ...

class BaseTransferMeta:
    @property
    def call_args(self) -> List[Any]: ...
    @property
    def transfer_id(self) -> str: ...
    @property
    def user_context(self) -> Dict[str, Any]: ...

class TransferFuture(BaseTransferFuture):
    def __init__(
        self, meta: Optional[TransferMeta] = ..., coordinator: Optional[TransferCoordinator] = ...
    ) -> None: ...
    @property
    def meta(self) -> TransferMeta: ...
    def done(self) -> bool: ...
    def result(self) -> None: ...
    def cancel(self) -> None: ...
    def set_exception(self, exception: BaseException) -> None: ...

class TransferMeta(BaseTransferMeta):
    def __init__(
        self, call_args: Optional[Sequence[Any]] = ..., transfer_id: Optional[str] = ...
    ) -> None: ...
    @property
    def call_args(self) -> List[Any]: ...
    @property
    def transfer_id(self) -> str: ...
    @property
    def size(self) -> int: ...
    @property
    def user_context(self) -> Dict[str, Any]: ...
    def provide_transfer_size(self, size: int) -> None: ...

class TransferCoordinator:
    transfer_id: str
    def __init__(self, transfer_id: Optional[str] = ...) -> None: ...
    @property
    def exception(self) -> BaseException: ...
    @property
    def associated_futures(self) -> List[TransferFuture]: ...
    @property
    def failure_cleanups(self) -> List[TransferFuture]: ...
    @property
    def status(self) -> str: ...
    def set_result(self, result: str) -> None: ...
    def set_exception(self, exception: BaseException, override: bool = ...) -> None: ...
    def result(self) -> str: ...
    def cancel(self, msg: str = ..., exc_type: Type[BaseException] = ...) -> None: ...
    def set_status_to_queued(self) -> None: ...
    def set_status_to_running(self) -> None: ...
    def submit(
        self, executor: BoundedExecutor, task: Task, tag: Optional[TaskTag] = ...
    ) -> TransferFuture: ...
    def done(self) -> bool: ...
    def add_associated_future(self, future: TransferFuture) -> None: ...
    def remove_associated_future(self, future: TransferFuture) -> None: ...
    def add_done_callback(
        self, function: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> None: ...
    def add_failure_cleanup(
        self, function: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> None: ...
    def announce_done(self) -> None: ...

class BoundedExecutor:
    EXECUTOR_CLS: Type[BaseExecutor]
    def __init__(
        self,
        max_size: int,
        max_num_threads: int,
        tag_semaphores: Optional[Dict[str, Any]] = ...,
        executor_cls: Optional[Type[BaseExecutor]] = ...,
    ) -> None: ...
    def submit(
        self, task: Task, tag: Optional[TaskTag] = ..., block: bool = ...
    ) -> TransferFuture: ...
    def shutdown(self, wait: bool = ...) -> None: ...

class ExecutorFuture:
    def __init__(self, future: TransferFuture) -> None: ...
    def result(self) -> str: ...
    def add_done_callback(self, fn: Callable[[], Any]) -> None: ...
    def done(self) -> bool: ...

class BaseExecutor:
    def __init__(self, max_workers: Optional[int] = ...) -> None: ...
    def submit(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any: ...
    def shutdown(self, wait: bool = ...) -> None: ...

class NonThreadedExecutor(BaseExecutor):
    def submit(
        self, fn: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> NonThreadedExecutorFuture: ...
    def shutdown(self, wait: bool = ...) -> None: ...

class NonThreadedExecutorFuture:
    def __init__(self) -> None: ...
    def set_result(self, result: str) -> None: ...
    def set_exception_info(self, exception: BaseException, traceback: Any) -> None: ...
    def result(self, timeout: Optional[float] = ...) -> str: ...
    def done(self) -> bool: ...
    def add_done_callback(self, fn: Callable[..., Any]) -> None: ...

class TaskTag(NamedTuple):
    name: str

IN_MEMORY_UPLOAD_TAG: TaskTag
IN_MEMORY_DOWNLOAD_TAG: TaskTag