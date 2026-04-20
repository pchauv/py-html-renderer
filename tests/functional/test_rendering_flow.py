import datetime
from pathlib import Path

from py_html_renderer import HtmlRenderer, create_renderer


def test_end_to_end_rendering_with_translations_and_styles(tmp_path: Path):
    assets_path = tmp_path / "assets"
    templates_dir = assets_path / "templates"
    styles_dir = assets_path / "styles"

    templates_dir.mkdir(parents=True)
    styles_dir.mkdir(parents=True)

    # Création d'un template utilisant le filtre de date et le CSS injecté
    (templates_dir / "invoice.html").write_text("""
    <html>
    <head><style>{{ css }}</style></head>
    <body>
        <h1>Invoice</h1>
        <p>Date: {{ date | format_date('long') }}</p>
    </body>
    </html>
    """)

    # Création d'un fichier SASS
    (styles_dir / "invoice.scss").write_text("""
    $primary-color: #3498db;
    body { h1 { color: $primary-color; } }
    """)

    # Generation du rendu
    renderer: HtmlRenderer = create_renderer(assets_path, locale_str="fr_FR")
    html_output = renderer.generate("invoice", date=datetime.date(2026, 4, 20))

    # 1. Vérification du contenu (Babel a fonctionné)
    assert "20 avril 2026" in html_output

    # 2. Vérification du style (SASS a été compilé et injecté)
    # libsass compile généralement en minifié ou avec un format spécifique
    assert "color:#3498db" in html_output.replace(" ", "")

    # 3. Vérification de la structure HTML
    assert "<h1>Invoice</h1>" in html_output
