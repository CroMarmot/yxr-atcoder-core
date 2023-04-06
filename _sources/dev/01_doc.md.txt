# Doc

auto generate from code

```bash
sphinx-apidoc -o docs/ . -f
```

This will force overwriting the files list below

```text
docs/setup.rst.
docs/ac_core.rst.
docs/ac_core.interfaces.rst.
docs/ac_core.modal.rst.
docs/ac_core.utils.rst.
docs/tests.rst.
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
cd docs
sphinx-autobuild . ./_build/html/
```
