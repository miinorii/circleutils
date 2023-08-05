from setuptools import setup

setup(
    name="circleutils",
    author="miinorii",
    version="2023.7.15",
    packages=["circleutils"],
    install_requires=[
        "pydantic>=2.1.1",
        "polars>=0.18.12",
        "numpy>=1.25.2"
    ],
    python_requires=">=3.10"
)
