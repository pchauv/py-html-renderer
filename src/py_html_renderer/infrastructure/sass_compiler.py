from pathlib import Path

import sass

from ..domain.exceptions import ResourceNotFoundError, StyleCompilationError
from ..domain.ports import StyleCompiler


class SassCompiler(StyleCompiler):
    def __init__(self, styles_dir: Path):
        self.styles_dir = styles_dir
        self._cache: dict[str, str] = {}

    def compile(self, name: str) -> str:
        if name not in self._cache:
            path = self.styles_dir / f"{name}.scss"
            if not path.is_file():
                raise ResourceNotFoundError(f"File not found: {path}")

            try:
                result = sass.compile(filename=str(path))

            except sass.CompileError as e:
                raise StyleCompilationError(f"Compilation error : {str(e)}") from e

            if not result:
                raise StyleCompilationError(f"Generated CSS for '{name}' is empty.")

            self._cache[name] = result

        return self._cache[name]
