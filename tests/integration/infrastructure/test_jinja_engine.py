from pathlib import Path

from py_html_renderer.infrastructure.jinja_engine import JinjaTemplateEngine


def create_engine(tmp_path: Path, template_name: str, template_content: str) -> JinjaTemplateEngine:
    template_dir = tmp_path / "templates"
    template_dir.mkdir(parents=True, exist_ok=True)
    template_file = template_dir / f"{template_name}.html"
    template_file.write_text(template_content)

    return JinjaTemplateEngine(template_dir)


def test_jinja_integration_render_real_file(tmp_path: Path):
    engine = create_engine(tmp_path, "test", "Hello {{ name }}!")
    assert "Hello Python!" == engine.render("test", {"name": "Python"})


def test_jinja_integration_filter_works(tmp_path: Path):
    engine = create_engine(tmp_path, "filter", "Price: {{ val | format_price }}")
    engine.add_filter("format_price", lambda v: f"{v}€")

    assert "Price: 10€" == engine.render("filter", {"val": 10})
