# Dev

## Install dependencies

```
pip3 install -r requirements.txt
```

## Auto test

```
pytest
```

# Coverage test

```
coverage run -m pytest
```

## Coverage report

```
coverage html
```

## Auto formatting

```
yapf --in-place --recursive ac_core tests
```

## Build

```
python -m build
```

## Install at local for debug

```
cd <code folder>
pip3 install -e . --config-settings editable_mode=compat
```

https://github.com/microsoft/pylance-release/issues/3473

