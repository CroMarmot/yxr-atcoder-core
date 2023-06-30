# Auto Test

```bash
pytest -v
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

## Static gen

```bash
stubgen ac_core
```
