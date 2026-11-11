# Ticket CLI

A Python CLI application that reads ticket records from a JSON file, validates them using Pydantic, separates valid and invalid records, and logs the execution process.

The project brings together Python application structure, data validation, file handling, exception handling, logging, package management, and automated testing.

## Features

- Reads ticket records from a JSON file.
- Validates records using Pydantic.
- Separates valid and invalid tickets.
- Handles missing files and malformed JSON.
- Logs application execution and validation results.
- Includes automated tests using pytest.

## Project Structure

```text
ticket-cli/
│
├── data/
│   └── tickets.json
│
├── logs/
│   └── app.log
│
├── src/
│   └── ticket_cli/
│       ├── __init__.py
│       ├── cli.py
│       └── ticket.py
│
├── tests/
│   └── test_ticket.py
│
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

### Why this structure?

The project follows the **src layout**, a common approach for organizing Python packages.

- `src/` contains application source code.
- `ticket_cli/` is the actual Python package.
- `data/` contains input data.
- `logs/` stores generated application logs.
- `tests/` contains automated tests.

The distinction between `src/` and `ticket_cli/` is intentional.

We could put `cli.py` and `ticket.py` directly inside `src/`, but that would make them top-level modules rather than modules belonging to a dedicated application package.

Using `src/ticket_cli/` gives the application a clear package identity and makes package discovery and imports easier to manage.

The distribution name is `ticket-cli`, while the Python import name is `ticket_cli`. Hyphens are not used in Python import names.

## Application Workflow

```text
       tickets.json
             |
             v
        JSON Reading
             |
             v
      Pydantic Validation
             |
        +----+----+
        |         |
        v         v
      Valid     Invalid
     Tickets    Tickets
        |         |
        +----+----+
             |
             v
       Terminal Output
             |
             v
         Application
           Logs
```

Each ticket is validated independently. An invalid record does not prevent subsequent records from being processed.

### Ticket validation rules

| Field | Requirement |
|---|---|
| ID | Positive integer |
| Title | 5–100 characters |
| Priority | High, Medium, Low |
| Status | Open, In Progress, Resolved |

## Technical Decisions

### 1. Python package and imports

The application uses package-based imports instead of relying on the current working directory or manually modifying Python's module search path.

For example:

```python
from ticket_cli.ticket import Ticket
```

Inside the package, relative imports can be used:

```python
from .ticket import Ticket
```

The empty `__init__.py` identifies `ticket_cli` as a regular Python package.

### 2. Package configuration with `pyproject.toml`

`pyproject.toml` is used to define project metadata, dependencies, build configuration, and package discovery.

The project uses setuptools and discovers packages inside `src/`.

It also separates dependencies into:

- **Runtime:** Pydantic.
- **Development:** pytest.

This keeps the application dependencies separate from its testing tools.

### 3. Editable installation

The project is installed using:

```powershell
python -m pip install -e ".[dev]"
```

Editable installation registers the local project as an installed package while using the source files in the development directory.

This allows package imports to work without manually configuring `PYTHONPATH`.

Changes to the source code are reflected immediately without reinstalling the package.

### 4. Path management with `pathlib`

The application uses `pathlib` instead of hardcoded absolute paths.

Paths are constructed relative to the location of `cli.py`, using `__file__` and its parent directories.

This avoids depending on the terminal's current working directory.

For example, the application can locate:

- `data/tickets.json`
- `logs/app.log`

regardless of where the application is launched from, provided the project structure remains unchanged.

The `Path` object also provides methods for creating directories and working with files.

### 5. Logging

Python's built-in logging module records application activity.

The application uses:

| Level | Purpose |
|---|---|
| INFO | Application execution and processing progress |
| WARNING | Individual ticket validation failures |
| ERROR | File and JSON parsing failures |

Logs are stored in `logs/app.log`.

The application creates the logs directory automatically if it does not exist.

### 6. Exception handling

Errors are handled at the appropriate level:

- Pydantic `ValidationError` is handled per ticket so processing can continue.
- `FileNotFoundError` handles missing input files.
- `JSONDecodeError` handles malformed JSON.

This separates individual record validation failures from errors that prevent the application from reading its input.

## Testing

The project uses pytest for automated testing.

Run the tests from the project root:

```powershell
python -m pytest -v
```

The current test suite covers:

| Test scenario | Purpose |
|---|---|
| Valid ticket | Checks successful model creation |
| Invalid ticket | Checks Pydantic validation errors |
| Ticket separation | Checks valid and invalid record segregation |
| JSON reading | Checks successful file loading |
| Missing file | Checks file-not-found handling |
| Malformed JSON | Checks JSON parsing errors |
| Missing ticket ID | Checks application handling of records without IDs |

### Why `tmp_path`?

File-related tests use pytest's built-in `tmp_path` fixture.

It provides an isolated temporary directory for each test.

This allows tests to create their own JSON files, including missing-file and malformed-JSON scenarios, without modifying the application's actual input data.

## Installation and Execution

### Requirements

- Python 3.10 or newer.
- pip.

### Install dependencies and the package

From the project root:

```powershell
python -m pip install -e ".[dev]"
```

### Run the application

```powershell
python -m ticket_cli.cli
```

### Run tests

```powershell
python -m pytest -v
```

## Current Limitations

The application intentionally keeps its scope small.

Known limitations:

1. **Duplicate IDs:** Tickets are stored in dictionaries using their IDs as keys. Duplicate IDs can overwrite earlier records.
2. **Missing IDs:** Records without IDs use `"Unknown"` as their dictionary key. Multiple such records can overwrite one another.
3. **Invalid record preservation:** The application stores validation errors rather than the complete original invalid records.
4. **Fixed input location:** The JSON input path is currently defined inside the application. Users cannot specify a custom file through command-line arguments.
5. **Limited error handling:** Only the expected file and JSON parsing errors are explicitly handled.
6. **No process exit codes:** Application failures are logged but do not yet return explicit non-zero exit codes.
7. **No external integrations:** The application does not use a database, REST API, or LLM.

These limitations are acceptable for the current scope.

## Technology Stack

- Python
- Pydantic
- JSON
- pathlib
- logging
- pytest
- setuptools
- pyproject.toml

---

**Project goal:** Demonstrate a structured, testable Python CLI application with package management, data validation, file handling, logging, and exception handling.