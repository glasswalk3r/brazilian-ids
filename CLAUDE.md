# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Python 3 (>=3.10) package that validates and formats Brazilian identification numbers/documents: CNPJ, CPF,
CEP (postal code), Município (municipality codes), PIS/PASEP, CNO, NUPJ (labor lawsuit numbers), and SQL
("Sequencial de Quadra") for real estate. Zero runtime dependencies for normal use of the package (the
`extended_cep` module is the one exception — see below).

## Development commands

Dependency management uses [uv](https://docs.astral.sh/uv/). Dev tooling is declared in the `dev` group under
`[dependency-groups]` in `pyproject.toml` and pinned in `uv.lock`. Install with:
```
uv sync             # creates/updates .venv with runtime + dev dependencies
```
`requirements-dev.txt` predates this and is now redundant with the `dev` group — don't add new dev deps there.
`Makefile`'s `init` target (`pip install -r requirements-dev.txt`) also predates the uv migration and hasn't been
updated yet; prefer `uv sync` over `make init`.

Run project tools through `uv run` so they use the locked environment:
```
uv run pytest                            # equivalent to: make test
uv run pytest -v --cov                   # equivalent to: make coverage
uv run pytest tests/test_cep.py          # single test file
uv run pytest tests/test_cep.py::test_parse   # single test
```

Linting/formatting is done with **ruff** (`make lint` still invokes an older flake8 setup and is out of date):
```
uv run ruff check src/brazilian_ids tests
uv run ruff format src/brazilian_ids tests
```
Ruff config: line length 120, target `py312`, standard excludes (see `[tool.ruff]` in `pyproject.toml`).

Type checking:
```
uv run mypy src/brazilian_ids
```
`mypy.ini` sets `namespace_packages = True` — there are intentionally **no `__init__.py` files** anywhere under
`src/brazilian_ids`; the package relies on PEP 420 implicit namespace packages plus `pythonpath = ["src"]` in
`pyproject.toml` for pytest and `packages = ["src/brazilian_ids"]` for the hatchling build.

Version bumps use `bump-my-version` (`make bump` bumps patch version, still invoked via the system `bump-my-version`
rather than `uv run`), configured in `.bumpversion.toml`.

## Architecture

### Module layout

Code lives under `src/brazilian_ids/functions/<domain>/<id>.py`, grouped by real-world domain:

- `company/cnpj.py` — CNPJ
- `person/cpf.py`, `person/pis_pasep.py`
- `location/cep.py`, `location/extended_cep.py`, `location/municipio.py`, `location/states.py`
- `labor_dispute/nupj.py`
- `real_state/cno.py`, `real_state/sql.py`
- `functions/exceptions.py` — shared base exceptions
- `functions/util.py` — shared low-level helpers (e.g. `NONDIGIT_REGEX`)

Each ID module is self-contained and independently importable, e.g.
`from brazilian_ids.functions.location.cep import parse, is_valid`. There is no top-level re-export module —
callers import directly from the specific `<domain>.<id>` submodule.

### Per-ID conventions

Every ID module follows the same shape; when adding a new ID or extending an existing one, match it:

- **`is_valid(id: str, ...) -> bool`** — the core validation function. Strips non-digits via
  `brazilian_ids.functions.util.NONDIGIT_REGEX` first. Never raises for a malformed input, just returns `False`.
- **`format(id: str) -> str`** — applies the canonical human-readable formatting (e.g. `000.000.000-00` for CPF,
  `00000-000` for CEP). Raises the module's `Invalid*Error` if the input isn't valid.
- **`pad(id: str) -> str`** — zero-pads a partial/shortened ID back to full length, where applicable.
- **`random(formatted: bool = True) -> str`** — generates a random, valid instance of the ID, used for tests/demos.
- **`verification_digits(id: str) -> tuple[...]`** — computes check digit(s), where the ID uses check digits.

### Exceptions

All ID-specific errors derive from the shared base classes in `functions/exceptions.py`:

- `InvalidIdError(ValueError)` — abstract; subclasses must implement `id_type()` to name the ID kind in the
  default error message.
- `InvalidIdLengthError(InvalidIdError)` — for IDs with fewer digits than required; message reports how many
  digits were expected vs. found.

Each domain module defines its own `InvalidXTypeMixin` (implementing `id_type()`) and composes it with the base
errors via multiple inheritance, e.g.:
```python
class InvalidCpfTypeMixin:
    def id_type(self):
        return "CPF"

class InvalidCpfError(InvalidCpfTypeMixin, InvalidIdError): ...
class InvalidCpfLengthError(InvalidCpfTypeMixin, InvalidIdLengthError): ...
```
Follow this mixin pattern rather than duplicating `id_type()` in each exception class.

### `location/cep.py` vs `location/extended_cep.py`

- `cep.py` is dependency-free and holds the core `CEP` dataclass (frozen, with `__ge__`/`__le__` for range
  comparisons), `parse`/`format`/`is_valid`, and `is_valid_extended`, which checks a CEP against known per-state
  numeric ranges (`CepRange`, a singleton via the local `Singleton` metaclass) without any network access.
- `extended_cep.py` is the only module with third-party dependencies (`httpx`, `beautifulsoup4`) — it scrapes
  live CEP range data from Correios' website (`CepRangeHttpSource`) to validate/enumerate ranges more precisely
  than the static table in `cep.py`. These deps aren't declared in `pyproject.toml`'s `dependencies` — treat this
  module as optional/experimental and don't assume `httpx`/`bs4` are installed elsewhere in the package.

### Tests

Tests live in `tests/`, one file per ID (`test_<id>.py`) plus a companion `test_<id>_exceptions.py` for exception
classes. They import directly from the `src` module paths (enabled by `pythonpath = ["src"]`) — no package install
needed to run the suite. Use `pytest.fixture`/`pytest.mark.parametrize` in the existing style rather than
hand-rolled test data setup.
