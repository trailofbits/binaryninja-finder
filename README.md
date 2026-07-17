# binaryninja-finder

Automatically finds and adds Binary Ninja's Python API to `sys.path` at interpreter startup.

## Installation

```console
uv add binaryninja-finder
```

Once installed, `import binaryninja` will work in any script or REPL that uses the same Python environment.

For a one-off command, use `uv run --with` without adding the package to a project:

```console
uv run --with binaryninja-finder python -c 'import binaryninja; print(binaryninja.core_version())'
```

## Standalone scripts

Add [inline dependency metadata](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies) to make a Binary Ninja script runnable without a project or virtual environment:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["binaryninja-finder"]
# ///

import binaryninja

print(binaryninja.core_version())
```

Save it as `example.py`, then run it with `uv run example.py`. On systems that support shebangs, you can also make it executable with `chmod +x example.py` and run `./example.py` directly.

## How it works

The package installs a `.pth` file that runs automatically when Python starts. It checks whether `binaryninja` is already importable and, if not, searches for a local Binary Ninja installation and adds its `python/` directory to `sys.path`.

The search order is:

1. **`BN_INSTALL_DIR`** environment variable — points to the BN installation root
2. **`lastrun` file** — in the BN user config directory (written by Binary Ninja on launch)
3. **Common platform paths** — e.g. `/Applications/Binary Ninja.app` on macOS, `/opt/binaryninja` on Linux, `C:\Program Files\Vector35\BinaryNinja` on Windows

## Configuration

| Environment variable | Description |
|---|---|
| `BN_INSTALL_DIR` | Override the Binary Ninja installation directory |
| `BN_USER_DIRECTORY` | Override the Binary Ninja user config directory (where `lastrun` is stored) |

## License

See [LICENSE](LICENSE) for details.
