import datetime
from pathlib import Path

from py_html_renderer.application.renderer_factory import create_renderer
from py_html_renderer.domain.renderer import Renderer


def test_create_renderer_assembles_functional_parts(tmp_path: Path):
    """
    Vérifie que la factory crée un Renderer fonctionnel avec
    tous ses composants (Sass, Jinja, Babel) correctement branchés.
    """
    templates_dir = tmp_path / "templates"
    styles_dir = tmp_path / "styles"
    templates_dir.mkdir()
    styles_dir.mkdir()

    # Création d'un template qui utilise TOUTES les fonctionnalités
    # Note : On inclut {{ css }} pour valider l'injection du style
    (templates_dir / "test.html").write_text("""
        Style: {{ css }}
        Date: {{ my_date | format_date('full') }}
    """)

    # On crée un fichier SASS simple
    (styles_dir / "test.scss").write_text("body { color: red; }")

    # Création du moteur de rendu
    renderer = create_renderer(tmp_path, locale_str="en_US")

    # Vérification de l'instance
    assert isinstance(renderer, Renderer)

    # Génération du rendu
    dt = datetime.date(2023, 12, 25)
    result = renderer.generate("test", my_date=dt)

    # Vérification que Babel a formaté la date en anglais
    assert "Monday, December 25, 2023" in result

    # Vérification que Sass a été compilé et injecté par Jinja
    # (libsass retire souvent les espaces dans le rendu par défaut)
    assert "body{color:red;}" in result.replace(" ", "").replace("\n", "")


def test_create_renderer_with_different_locales(tmp_path: Path):
    """Vérifie que la factory configure correctement Babel selon la locale."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir(exist_ok=True)
    (tmp_path / "styles").mkdir(exist_ok=True)

    (templates_dir / "locale_test.html").write_text("{{ d | format_date('short') }}")
    dt = datetime.date(2023, 12, 25)

    # Test en français
    renderer_fr = create_renderer(tmp_path, locale_str="fr_FR")
    assert "25/12/2023" in renderer_fr.generate("locale_test", d=dt)

    # Test en américain
    renderer_us = create_renderer(tmp_path, locale_str="en_US")
    assert "12/25/23" in renderer_us.generate("locale_test", d=dt)
