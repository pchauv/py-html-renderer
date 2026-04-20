import logging
from typing import Any

from .exceptions import ResourceNotFoundError
from .ports import HtmlRenderer, StyleCompiler, TemplateEngine

logger = logging.getLogger(__name__)


class Renderer(HtmlRenderer):
    def __init__(self, engine: TemplateEngine, compiler: StyleCompiler) -> None:
        self.engine: TemplateEngine = engine
        self.compiler: StyleCompiler = compiler

    def generate(self, template_name: str, **data: Any) -> str:
        context = data
        try:
            data["css"] = self.compiler.compile(template_name)
        except ResourceNotFoundError:
            logger.warning(f"No SCSS file found for {template_name}, proceeding without styles.")
        result = self.engine.render(template_name, context)
        if not isinstance(result, str):
            raise TypeError(f"Renderer expected a string from engine, got {type(result)}")
        return result
