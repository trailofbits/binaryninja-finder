from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


def _user_dir() -> Path:
    bn_user_dir = os.environ.get("BN_USER_DIRECTORY")
    if bn_user_dir:
        return Path(bn_user_dir)
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Binary Ninja"
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        return Path(appdata) / "Binary Ninja"
    return Path.home() / ".binaryninja"


def _common_paths() -> list[Path]:
    if sys.platform == "linux":
        return [
            Path("/opt/binaryninja/python"),
            Path.home() / "binaryninja" / "python",
        ]
    if sys.platform == "darwin":
        return [Path("/Applications/Binary Ninja.app/Contents/Resources/python")]
    if sys.platform == "win32":
        return [Path("C:/Program Files/Vector35/BinaryNinja/python")]
    return []


def _python_dir(install_dir: Path) -> Path:
    if sys.platform == "darwin":
        return install_dir / "Contents" / "Resources" / "python"
    return install_dir / "python"


def _find_binary_ninja(*, validate: bool = True) -> Path | None:
    """Find the Binary Ninja Python API directory."""
    candidates: list[Path] = []

    env_install = os.environ.get("BN_INSTALL_DIR")
    if env_install:
        p = Path(env_install)
        candidates.append(_python_dir(p))

    try:
        install_dir = Path((_user_dir() / "lastrun").read_text().strip())
        candidates.append(_python_dir(install_dir))
    except OSError:
        pass

    for path in candidates:
        if not validate or (path / "binaryninja" / "__init__.py").is_file():
            return path

    for path in _common_paths():
        if (path / "binaryninja" / "__init__.py").is_file():
            return path

    return None


def _setup() -> None:
    if importlib.util.find_spec("binaryninja") is not None:
        return
    if (path := _find_binary_ninja()) is not None:
        sys.path.append(str(path))
