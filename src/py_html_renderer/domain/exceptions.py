class RendererError(Exception):
    """Base exception"""

    pass


class StyleCompilationError(RendererError):
    """Erreur lors de la compilation SCSS"""

    pass


class ResourceNotFoundError(RendererError):
    """Fichier introuvable"""

    pass
