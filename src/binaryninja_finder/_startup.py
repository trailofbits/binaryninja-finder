def _setup():
    import importlib.util

    if importlib.util.find_spec("binaryninja") is not None:
        return

    from binaryninja_finder._finder import find_binary_ninja

    path = find_binary_ninja()
    if path is not None:
        import sys

        sys.path.append(str(path))


try:
    _setup()
except Exception:
    pass
