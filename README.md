# binaryninja-finder

Automatically finds and adds Binary Ninja's Python API to `sys.path` at interpreter startup — no manual path manipulation needed.

## Installation

```
pip install binaryninja-finder
```

Or with [uv](https://docs.astral.sh/uv/):

```
uv add binaryninja-finder
```

Once installed, `import binaryninja` will work in any script or REPL that uses the same Python environment.

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

## Programmatic usage

You can also use the finder directly:

```python
from binaryninja_finder._finder import find_binary_ninja

path = find_binary_ninja()
if path:
    print(f"Found Binary Ninja Python API at: {path}")
```

## License

See [LICENSE](LICENSE) for details.
