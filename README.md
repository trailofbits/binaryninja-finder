# binaryninja-finder

Automatically finds and adds Binary Ninja's Python API to `sys.path` at interpreter startup.

## Installation

```
pip install git+https://github.com/trailofbits/binaryninja-finder
```

Or with [uv](https://docs.astral.sh/uv/):

```
uv add git+https://github.com/trailofbits/binaryninja-finder
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

## License

See [LICENSE](LICENSE) for details.
