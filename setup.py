from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="api-cataloger",
    version="0.1.0",
    author="The Pals Lab",
    description="Automatically parses OpenAPI specs, controller files, or annotations and generates a searchable internal catalog of APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "jsonschema>=4.0.0",
        "click>=8.0.0",
        "jinja2>=3.0.0",
        "gitpython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "api-cataloger=api_cataloger.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
