from unittest.mock import MagicMock

import pytest

from py_html_renderer.domain.ports import StyleCompiler, TemplateEngine
from py_html_renderer.domain.renderer import Renderer


@pytest.fixture
def mock_engine() -> MagicMock:
    """Mock du moteur de template."""
    return MagicMock(spec=TemplateEngine)


@pytest.fixture
def mock_compiler() -> MagicMock:
    """Mock du compilateur Sass."""
    return MagicMock(spec=StyleCompiler)


@pytest.fixture
def renderer(mock_engine: MagicMock, mock_compiler: MagicMock) -> Renderer:
    """Instance du Renderer injectée avec les mocks."""
    return Renderer(engine=mock_engine, compiler=mock_compiler)


def test_generate_should_assemble_css_and_data_into_context(
    renderer: Renderer, mock_engine: MagicMock, mock_compiler: MagicMock
) -> None:
    template_name = "invoice"
    fake_css = "body { color: red; }"
    fake_html = "<html><body>Content</body></html>"
    user_data = {"name": "Alice", "amount": 150}

    # Définition des retours des mocks
    mock_compiler.compile.return_value = fake_css
    mock_engine.render.return_value = fake_html

    result = renderer.generate(template_name, **user_data)

    # 1. Vérification que le compilateur a été appelé avec le bon nom
    mock_compiler.compile.assert_called_once_with(template_name)

    # 2. Vérification que le moteur de rendu a reçu les données fusionnées (CSS + DATA)
    expected_context = {"name": "Alice", "amount": 150, "css": fake_css}
    mock_engine.render.assert_called_once_with(template_name, expected_context)

    # 3. Vérification que le résultat final est bien celui du moteur
    assert result == fake_html
    assert isinstance(result, str)


def test_generate_should_raise_error_if_engine_does_not_return_str(
    renderer: Renderer, mock_engine: MagicMock
) -> None:
    # Simulation d'un bug : le moteur renvoie None ou un int
    mock_engine.render.return_value = None

    # Vérification que 'assert isinstance' dans le code lève bien une AssertionError
    with pytest.raises(TypeError, match="expected a string"):
        renderer.generate("any_template")
