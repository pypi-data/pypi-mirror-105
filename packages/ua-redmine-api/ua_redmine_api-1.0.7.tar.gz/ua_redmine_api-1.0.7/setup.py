import os
from setuptools import setup, find_packages


def readme(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as file:
        return file.read()


setup(
    name="ua_redmine_api",
    version="1.0.7",
    packages=find_packages(),
    author="Ryan Johannes-Bland",
    author_email="rjjohannesbland@email.arizona.edu",
    description=(
        "Provides easy interface for making REST requests to University of "
        "Arizona RII Redmine database."
    ),
    long_description=readme("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/UACoreFacilitiesIT/UA-Redmine-API",
    license="MIT",
    install_requires=["requests"],
)
