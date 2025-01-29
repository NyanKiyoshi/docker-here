# Running Tests

## Using `make` & Containers

> [!NOTE]
> 
> This is only for Unix-like systems, it will only work if you have the `make`
> command installed.

Either run:
- `make test`
- Or:

  1. `make shell`
  2. `poetry run pytest`

  This method avoids installing dependencies multiple times if
  you are actively developing.

## Natively Using Python

1. Install Python ≥ 3.12
2. Install dependencies:
   ```bash
   $ pip install poetry
   $ poetry install
   ```
3. Run tests:
   ```bash
   $ poetry run pytest
   ```

