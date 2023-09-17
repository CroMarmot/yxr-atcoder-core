# Auto Test

```bash
pytest -v tests/unit
# config tests/e2e/cfg.py first (Read tests/e2e/README.md)
pytest -v tests/e2e
pytest -v tests/e2e/test_auth.py::test_auth
```

## Coverage test

```bash
coverage run -m pytest
```

## Coverage report

```bash
coverage html
```

## Static type test

```bash
mypy --ignore-missing-imports ac_core tests
```
