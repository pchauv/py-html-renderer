.DEFAULT_GOAL := install

.PHONY: install lint test pre-push help

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Installation de UV et des dépendances
	@if ! command -v uv > /dev/null; then \
		echo "Installation de uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	uv python install
	uv sync

lint: ## Outils de qualité (Ruff + Mypy)
	uv run ruff check --fix .
	uv run ruff format .
	uv run mypy src

test: ## Tests (Unit -> Integration -> Functional) avec arrêt au premier échec
	uv run pytest tests/unit && \
	uv run pytest tests/integration && \
	uv run pytest tests/functional

pre-push: ## Qualité et Tests (à lancer avant de push)
	@${MAKE} lint
	@${MAKE} test