import logging, sys, traceback, os
from types import TracebackType
from typing import Type, TypeVar, Protocol

__all__ = ['global_exception_handler']

T = TypeVar('T', bound=str)
class SuportsWrite(Protocol[T]):
    def write(self, s: T) -> None: ...

def global_exception_handler(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
    /,
    logger: logging.Logger | None = None,
    file: SuportsWrite[str] | None = None, # where to write the exception summary message
    system_cls: bool = False
) -> None:

    """
    A global exception handler that handles uncaught exceptions in the application. 

    This function is invoked whenever an uncaught exception occurs. It provides a summary
    of the exception, including its type, file, and line number, and writes this summary to
    the specified output, such as a log file or the console. Additionally, it logs the full
    traceback of the exception for debugging purposes.

    Args:
        `exc_type (Type[BaseException])`: The type of the exception raised.
        `exc_value (BaseException)`: The exception instance.
        `exc_traceback (TracebackType | None)`: The traceback object, or `None` if no traceback is available.
        `logger (logging.Logger | None, optional)`: A logger to log the exception details. Defaults to the root logger.
        `file (SuportsWrite[str] | None, optional)`: A file-like object to write the exception summary. Defaults to `sys.stdout` (console).
        `system_cls (bool, optional)`: If `True`, clears the terminal screen before displaying the exception summary. Defaults to `False`.

    Returns:
        None: This function does not return any value.

    Side effects:
        - Logs the full exception traceback using the provided logger.
        - Writes the exception summary to the specified output (console or file).
        - Clears the terminal screen if `system_cls` is True.

    Notes:
        - The exception summary message is colorized in red for visibility.
        - If the exception is a KeyboardInterrupt, the default exception handler is used instead.
        - The `file` argument must be a writable file-like object that supports the `write` method.

    """

    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    file: SuportsWrite = sys.stdout if file is None else file # defaults to the terminal.
    logger: logging.Logger = logging if logger is None else logger

    #extracts the last traceback frame
    if exc_traceback:
        tb_last_frame: object = traceback.extract_tb(exc_traceback)[-1]
        file_name: str = tb_last_frame.filename
        line_number: int = tb_last_frame.lineno
    else:
        file_name: str = '<unkown file>'
        line_number: int = -1

    base_folder = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.relpath(os.path.abspath(file_name), start=os.path.abspath(base_folder))
    relative_path = relative_path.strip('./')

    exception_summary: str = (
        "\033[1;31mAn unexpected error occurred: {} at {}: {}. Check the log file for details.\033[0m"
    ).format(exc_type.__name__, relative_path, line_number)

    if system_cls:
        os.system('cls')

    logger.exception("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    file.write(exception_summary + "\n")