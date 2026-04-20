from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class TemplateEngine(ABC):
    @abstractmethod
    def render(self, template_name: str, context: dict[str, Any]) -> str:
        pass

    @abstractmethod
    def add_filter(self, name: str, func: Callable[..., str]) -> None:
        """Enregistre un filtre personnalisé utilisable dans les templates."""
        pass


class StyleCompiler(ABC):
    @abstractmethod
    def compile(self, name: str) -> str:
        pass


class AssetProvider(ABC):
    @abstractmethod
    def get_asset_b64(self, name: str) -> str:
        pass


class HtmlRenderer(ABC):
    @abstractmethod
    def generate(self, template_name: str, **data: Any) -> str:
        pass
