.DEFAULT_GOAL := install

install: ## Installation de UV et des dépendances
	@if ! command -v uv > /dev/null; then \
		echo "Installation de uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	uv python install
	uv sync

run: ## Lance l'application
	uv run python src/main.py

pre-push: ## Qualité et Tests (à lancer avant de push)
	uv run ruff check --fix src
	uv run ruff format src
	uv run mypy src
	uv run pytest tests/