from setuptools import setup, find_packages

setup(
    name="multi-framework-agent",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        # Add dependencies here
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "ruff",
            "mypy",
        ],
    },
)