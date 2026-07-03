### Exit Codes Overview

Understanding exit codes is crucial when dealing with shell commands:

| Exit Code | Description                                   |
|-----------|-----------------------------------------------|
| 0         | Success: The command completed successfully.  |
| 1         | General error: Catchall for general errors.   |
| 2         | Misuse of shell builtins (e.g., `cd`).        |
| 126       | Command invoked cannot execute.               |
| 127       | Command not found.                            |
| 128       | Invalid argument to exit.                     |
| 130       | Script terminated by Control-C.               |
| 137       | Script terminated by `kill` (or OOM).         |
| 139       | Segmentation fault.                           |
| 141       | Script terminated by `kill -13` (SIGPIPE).    |
| 143       | Script terminated by `kill -15` (SIGTERM).    |
| 255       | Exit status out of range (exceeds 255).       |

