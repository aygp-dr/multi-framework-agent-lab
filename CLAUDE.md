#+TITLE: Claude Code Guidelines
#+AUTHOR: aygp-dr
#+DATE: 2025-05-20
#+PROPERTY: header-args :mkdirp yes :session *Python* :results output

* Build/Test/Lint Commands
- Virtual env :: =make .venv= creates environment with dependencies from pyproject.toml
- Dev setup :: =make setup-dev= installs all dependencies including dev tools and all frameworks
- Run agent :: =make framework-{framework_name}= automatically activates venv and runs agent
- Test all :: =make test= automatically activates venv and runs tests
- Test single :: =pytest tests/test_file.py::test_function= (with activated venv)
- Compare all :: =make compare= runs all framework implementations and compares them
- Clean project :: =make clean= removes artifacts, =make clean-venv= removes virtual environment
- Org tangle :: =make tangle= extracts code blocks from org files
- Org detangle :: Manual process using Emacs org-babel-detangle function

* Build System Dependencies
The Makefile uses file-level dependencies to manage the build process:
- =README.md= is generated from =README.org= and is gitignored
- =.venv= depends on =README.md= and =pyproject.toml=
- All framework targets depend on =.venv=
- =PYTHON= variable automatically activates venv and uses =uv run python=
- All commands that use Python use the =PYTHON= variable

* Code Style Guidelines
- Python version :: 3.11 (specified in pyproject.toml)
- Python execution :: Use =uv run python= via the =PYTHON= Makefile variable
- Imports :: Use absolute imports, group (stdlib, third-party, local) with a blank line between groups
- Formatting :: Follow PEP 8, use 4-space indentation
- Types :: Use type hints for function parameters and return values (Pydantic models preferred)
- Naming :: snake_case for variables/functions, PascalCase for classes
- Error handling :: Use specific exception types, avoid bare excepts
- Documentation :: Use docstrings for modules, classes, and functions (Google style)
- Framework implementation :: Follow BaseAgent interface in agents/base_agent.py
- Tools :: Use common tool implementations from common/tools.py
- LLM calls :: Use the wrapper in common/llm.py for consistency across frameworks
- Use Org mode with Babel for documentation and literate programming
- Org files :: Use =:tangle yes= property for code blocks to extract with make tangle