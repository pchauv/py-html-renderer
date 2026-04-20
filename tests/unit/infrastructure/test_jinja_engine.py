from pathlib import Path
from unittest.mock import patch

import pytest

from py_html_renderer.infrastructure.jinja_engine import JinjaTemplateEngine


@pytest.mark.parametrize(
    "input_name, expected_filename",
    [
        pytest.param("my_template", "my_template.html", id="simple"),
        pytest.param("my_template.html", "my_template.html", id="already_has_extension"),
    ],
)
def test_render_filename_logic(input_name, expected_filename):
    with patch("py_html_renderer.infrastructure.jinja_engine.Environment") as mock_env_class:
        mock_env = mock_env_class.return_value
        engine = JinjaTemplateEngine(Path("/fake/path"))

        engine.render(input_name, {})

        mock_env.get_template.assert_called_once_with(expected_filename)
