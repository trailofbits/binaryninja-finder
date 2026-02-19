from __future__ import annotations

import os
import sys
from pathlib import Path


def _user_directory() -> Path:
    """Return the Binary Ninja user configuration directory."""
    env = os.environ.get("BN_USER_DIRECTORY")
    if env:
        return Path(env)

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Binary Ninja"
    if sys.platform == "win32":
        return Path(os.environ.get("APPDATA", "")) / "Binary Ninja"
    return Path.home() / ".binaryninja"


def _python_dir_from_install(install_dir: Path) -> Path:
    """Derive the python/ directory from a BN installation root."""
    if sys.platform == "darwin" and install_dir.suffix == ".app":
        return install_dir / "Contents" / "Resources" / "python"
    return install_dir / "python"


def _validate(candidate: Path) -> bool:
    """Check that a candidate directory actually contains the BN Python API."""
    return (candidate / "binaryninja" / "__init__.py").is_file()


def _from_env() -> Path | None:
    """Check BN_INSTALL_DIR environment variable."""
    env = os.environ.get("BN_INSTALL_DIR")
    if not env:
        return None
    return _python_dir_from_install(Path(env))


def _from_lastrun() -> Path | None:
    """Read the lastrun file to find the BN installation."""
    lastrun = _user_directory() / "lastrun"
    try:
        text = lastrun.read_text().strip()
    except OSError:
        return None
    if not text:
        return None
    binary_path = Path(text)
    install_dir = binary_path.parent
    return _python_dir_from_install(install_dir)


def _from_common_paths() -> Path | None:
    """Check common platform-specific installation paths."""
    candidates: list[Path] = []

    if sys.platform == "linux":
        candidates.append(Path("/opt/binaryninja/python"))
        candidates.append(Path.home() / "binaryninja" / "python")
    elif sys.platform == "darwin":
        candidates.append(Path("/Applications/Binary Ninja.app/Contents/Resources/python"))
    elif sys.platform == "win32":
        candidates.append(Path("C:/Program Files/Vector35/BinaryNinja/python"))

    for candidate in candidates:
        if _validate(candidate):
            return candidate
    return None


def find_binary_ninja(*, validate: bool = True) -> Path | None:
    """Find the Binary Ninja Python API directory.

    Search order:
        1. BN_INSTALL_DIR environment variable
        2. lastrun file in BN user directory
        3. Common platform-specific paths

    Args:
        validate: If True, verify that the candidate directory contains
            binaryninja/__init__.py before returning it.

    Returns:
        Path to the directory containing the ``binaryninja`` package,
        or None if not found.
    """
    for searcher in (_from_env, _from_lastrun, _from_common_paths):
        path = searcher()
        if path is None:
            continue
        if not validate or _validate(path):
            return path
    return None
