.PHONY: setup test compare clean all activate .venv venv tangle detangle

all: setup test compare

.venv:
	uv venv

venv: .venv

activate: .venv
	@echo "To activate the virtual environment, run:"
	@echo "source .venv/bin/activate"

setup: .venv
	uv pip install -r requirements.txt

test:
	pytest tests/

compare:
	python -m evaluation.compare_all

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

clean-venv:
	rm -rf .venv

# Org mode tangle/detangle targets
tangle:
	emacs --batch --eval "(require 'org)" --eval "(org-babel-tangle-file \"SETUP.org\")" --eval "(org-babel-tangle-file \"README.org\")"

detangle:
	@echo "Detangling org files not automated. Use Emacs command org-babel-detangle manually."

framework-agno:
	python -m agents.agno.run

framework-dspy:
	python -m agents.dspy.run

framework-google-adk:
	python -m agents.google_adk.run

framework-inspect-ai:
	python -m agents.inspect_ai.run

framework-langgraph-functional:
	python -m agents.langgraph_functional.run

framework-langgraph-high-level:
	python -m agents.langgraph_high_level.run

framework-pydantic-ai:
	python -m agents.pydantic_ai.run

framework-smolagents:
	python -m agents.smolagents.run

framework-no-framework:
	python -m agents.no_framework.run
