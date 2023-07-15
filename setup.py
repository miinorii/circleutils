from setuptools import setup

setup(
    name="circleutils",
    author="miinorii",
    version="2023.7.15",
    packages=["circleutils"],
    install_requires=[
        "pydantic>=2.0",
        "pandas>=2.0.3",
        "numpy>=1.24.0"
    ]
)
