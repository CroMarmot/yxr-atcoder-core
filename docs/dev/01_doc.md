# Doc

auto generate from code

```bash
sphinx-apidoc -f -o docs/ ac_core/
```

This will force overwriting the files list below

```text
docs/ac_core.rst.
docs/ac_core.interfaces.rst.
docs/ac_core.modal.rst.
docs/ac_core.utils.rst.
docs/modules.rst.
```

## Generate static html doc

```bash
cd docs
make html
```

The output file is at `./docs/_build/html/`

## Live doc

```bash
cd docs && make clean && cd .. && sphinx-apidoc -f -o docs/ ac_core/ && cd docs && make html && cd ..
```
