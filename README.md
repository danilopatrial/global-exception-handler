
# Global Exception Handler Library

## Overview
The **Global Exception Handler Library** provides a centralized way to catch and log uncaught exceptions in Python applications. It logs detailed error messages and traceback information while also allowing user-friendly output to the console or a file.

## Features
- Logs uncaught exceptions to a file or a logger.
- Provides clear and user-friendly error messages in the console.
- Supports terminal clearing before displaying errors.
- Handles `KeyboardInterrupt` gracefully without logging.
- Extracts file names and line numbers for easier debugging.

## Installation
You can install the library using:

```sh
pip install global-exception-handler-func
```

## Usage
To use the global exception handler, import and set it as the default exception hook:

```python
import logging
import sys
from global_exception_handler import global_exception_handler

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR)
logger = logging.getLogger(__name__)

# Set the global exception hook
sys.excepthook = lambda exc_type, exc_value, exc_traceback: global_exception_handler(
    exc_type, exc_value, exc_traceback, logger=logger, system_cls=True
)

# Example of an error
raise ValueError("This is a test error")
```

## Function Reference

### `global_exception_handler`

#### Parameters:
- **`exc_type (BaseException)`**: The type of exception raised.
- **`exc_value (BaseException)`**: The actual exception instance.
- **`exc_traceback (TracebackType | None)`**: The traceback object, if available.
- **`logger (logging.Logger | None)`**: A logging instance to log error details.
- **`file (SupportsWrite[str] | None)`**: Where to write the summarized error message (default: `sys.stdout`).
- **`system_cls (bool)`**: If `True`, clears the terminal before printing the error message.

#### Example:
```python
import logging

logger = logging.getLogger("error_logger")
logger.setLevel(logging.ERROR)

try:
    1 / 0  # Example error
except Exception as e:
    global_exception_handler(type(e), e, e.__traceback__, logger=logger)
```

## License
This library is licensed under the MIT License.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## Author
**Danilo Patrial**
