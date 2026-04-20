# Moteur de rendu HTML

Basé sur le moteur de templates **Jinja** et avec compilation **scss**

---

## 🚀 Installation

````bash
pip install py-html-renderer
````

---

## 🚀 Utilisation Rapide

### 1. Structure des ressources à respecter
```text
my_assets/
├── templates/
│   └── invoice.html
└── styles/
    └── invoice.scss
```

### 2. Exemple de code
```python
import datetime
from pathlib import Path
from py_html_renderer import create_renderer, HtmlRenderer

# Initialisation
renderer: HtmlRenderer = create_renderer(
    assets_path=Path("my_assets"),
    locale_str="fr_FR"
)

# Génération du HTML
html: str = renderer.generate(
    "invoice",
    client_name="Pierre",
    date=datetime.date.today()
)
```

### 3. Templates & Styles

#### Injection CSS automatique
Dans le template invoice.html, la variable `{{ css }}` permet d'injecter le contenu compilé
de l'éventuelle feuille de style invoice.scss

```html
<html>
<head>
    <style>
        {{ css }}
    </style>
</head>
<body>
    <h1>Facture pour {{ client_name }}</h1>
    <p>Émise le : {{ date | format_date('long') }}</p>
</body>
</html>
```

---

## ⚙️ Développement

Le projet utilise `uv` pour la gestion des dépendances et un `Makefile` pour automatiser les tâches courantes.

### Installation de l'environnement
```bash
make install
```

### Qualité du code (Linting & Typage)
```bash
make lint
```

### Lancement des tests
Le projet suit une pyramide de tests (Unitaires -> Intégration -> Fonctionnels).
```bash
make test
```

### Avant de soumettre une modification
```bash
make pre-push
```
(Qualité puis tests)

---

## 📄 Licence

Distribué sous la licence MIT.

**Développé avec ❤️ par Pierre Chauvelot**