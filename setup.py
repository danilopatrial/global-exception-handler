from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='global_exception_handler_func',
    version='1.4',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown"
)