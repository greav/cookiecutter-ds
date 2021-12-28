from setuptools import find_packages, setup


def load_long_description():
    with open("README.md", encoding="utf-8") as f:
        text = f.read()
    return text


setup(
    name="{{ cookiecutter.package_name }}",
    packages=find_packages(),
    version="0.1.0",
    author="{{ cookiecutter.author_name }}",
    description="{{ cookiecutter.description }}",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
)
