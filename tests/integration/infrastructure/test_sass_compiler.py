from pathlib import Path

import pytest

from py_html_renderer.infrastructure.sass_compiler import SassCompiler


@pytest.fixture
def sass_dir(tmp_path: Path) -> Path:
    d = tmp_path / "scss"
    d.mkdir()
    return d


def test_sass_integration_compiles_valid_scss(sass_dir: Path):
    # Création d'un fichier avec variables
    scss_content = "$color: #ff0000; body { color: $color; }"
    (sass_dir / "main.scss").write_text(scss_content)
    compiler = SassCompiler(sass_dir)

    css_output = compiler.compile("main")

    assert "color: #ff0000" in css_output
    assert "body" in css_output


def test_sass_integration_handles_imports(sass_dir: Path):
    # Un fichier qui en importe un autre (test de load_paths)
    (sass_dir / "_vars.scss").write_text("$primary: blue;")
    (sass_dir / "app.scss").write_text("@import 'vars'; div { color: $primary; }")

    compiler = SassCompiler(sass_dir)

    css_output = compiler.compile("app")

    assert "color: blue" in css_output
