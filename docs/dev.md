# Dev

## Install dependencies

```bash
pip3 install -r requirements.txt
```

## Auto test

```bash
pytest
```

# Coverage test

```bash
coverage run -m pytest
```

## Coverage report

```bash
coverage html
```

## Static type test

```bash
mypy ac_core
```

## Static gen

```bash
stubgen ac_core
```

## Auto formatting

```bash
yapf --in-place --recursive ac_core tests
```

## Build

```bash
python -m build
```

## Install at local for debug

```
cd <code folder>
pip3 install -e . --config-settings editable_mode=compat
```

https://github.com/microsoft/pylance-release/issues/3473

