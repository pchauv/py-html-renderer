from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from py_html_renderer.domain.exceptions import ResourceNotFoundError
from py_html_renderer.infrastructure.sass_compiler import SassCompiler


def test_compile_raises_not_found_if_file_missing():
    compiler = SassCompiler(Path("/fake"))
    with pytest.raises(ResourceNotFoundError):
        compiler.compile("missing")


def test_compile_uses_cache_after_first_call():
    # Mock de 'sass_embedded.compile_string'
    with patch("sass.compile") as mock_sass:
        # Configuration du mock
        mock_result = MagicMock()
        mock_result.output = "body { color: red; }"
        mock_result.error = None
        mock_sass.return_value = mock_result

        # Création d'un vrai fichier temporaire pour passer le check 'is_file()'
        with (
            patch("pathlib.Path.is_file", return_value=True),
            patch("pathlib.Path.read_text", return_value="$c: red; body { color: $c; }"),
        ):
            compiler = SassCompiler(Path("/fake"))

            # Deux appels consécutifs
            compiler.compile("style")
            compiler.compile("style")

            # Vérification que sass_embedded n'a été appelé QU'UNE SEULE FOIS
            assert mock_sass.call_count == 1
