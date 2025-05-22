.PHONY: setup test compare clean all activate venv tangle detangle setup-dev

# Define PYTHON command to activate venv and run python
PYTHON=@. .venv/bin/activate && uv run python

all: setup test compare

# File-level dependency: README.md depends on README.org
README.md: README.org
	@echo "Converting README.org to README.md..."
	@emacs --batch --eval "(require 'ox-md)" --eval "(find-file \"README.org\")" --eval "(org-md-export-to-markdown)" --kill

# File-level dependency: .venv depends on pyproject.toml and README.md
.venv: README.md pyproject.toml
	@echo "Creating virtual environment with uv..."
	@uv venv
	@touch .venv

venv: .venv

activate: .venv
	@echo "To activate the virtual environment, run:"
	@echo "source .venv/bin/activate"

# Setup now depends on the .venv which depends on README.md
setup: .venv
	@echo "Installing dependencies from pyproject.toml..."
	@. .venv/bin/activate && uv pip install -e .

setup-dev: .venv
	@echo "Installing development dependencies..."
	@. .venv/bin/activate && uv pip install -e ".[dev,all]"

test: .venv
	$(PYTHON) -m pytest tests/

compare: .venv
	$(PYTHON) -m evaluation.compare_all

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -f README.md

clean-venv:
	rm -rf .venv

# Org mode tangle/detangle targets
tangle: README.org SETUP.org
	@echo "Tangling org files..."
	@emacs --batch --eval "(require 'org)" --eval "(org-babel-tangle-file \"SETUP.org\")" --eval "(org-babel-tangle-file \"README.org\")"

detangle:
	@echo "Detangling org files not automated. Use Emacs command org-babel-detangle manually."

# Framework targets - all depend on having a virtual environment
framework-agno: .venv
	$(PYTHON) -m agents.agno.run

framework-dspy: .venv
	$(PYTHON) -m agents.dspy.run

framework-google-adk: .venv
	$(PYTHON) -m agents.google_adk.run

framework-inspect-ai: .venv
	$(PYTHON) -m agents.inspect_ai.run

framework-langgraph-functional: .venv
	$(PYTHON) -m agents.langgraph_functional.run

framework-langgraph-high-level: .venv
	$(PYTHON) -m agents.langgraph_high_level.run

framework-pydantic-ai: .venv
	$(PYTHON) -m agents.pydantic_ai.run

framework-smolagents: .venv
	$(PYTHON) -m agents.smolagents.run

framework-no-framework: .venv
	$(PYTHON) -m agents.no_framework.run
