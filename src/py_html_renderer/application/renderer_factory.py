from pathlib import Path

import babel
import babel.dates

from ..domain.renderer import Renderer
from ..infrastructure.jinja_engine import JinjaTemplateEngine
from ..infrastructure.sass_compiler import SassCompiler


def create_renderer(assets_path: Path, locale_str: str = "fr_FR") -> Renderer:
    engine = JinjaTemplateEngine(assets_path / "templates")
    compiler = SassCompiler(assets_path / "styles")

    locale = babel.Locale.parse(locale_str)
    engine.add_filter(
        "format_date",
        lambda date, fmt: babel.dates.format_date(date, fmt, locale=locale),
    )

    return Renderer(engine=engine, compiler=compiler)
