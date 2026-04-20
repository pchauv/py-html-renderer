from collections.abc import Callable
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from ..domain.ports import TemplateEngine


class JinjaTemplateEngine(TemplateEngine):
    def __init__(self, templates_dir: Path):
        self._env = Environment(loader=FileSystemLoader(templates_dir))

    def add_filter(self, name: str, func: Callable[..., str]) -> None:
        self._env.filters[name] = func

    def render(self, template_name: str, context: dict[str, Any]) -> str:
        name = f"{template_name}.html" if not template_name.endswith(".html") else template_name
        template = self._env.get_template(name)

        return template.render(**context)
