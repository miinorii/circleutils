from setuptools import setup

setup(
    name="circleutils",
    author="miinorii",
    version="2023.8.5",
    description="Collection of tools for osu! related file manipulation",
    long_description="Collection of tools for osu! related file manipulation",
    url="https://github.com/miinorii/circleutils",
    packages=["circleutils"],
    install_requires=[
        "pydantic>=2.1.1",
        "polars>=0.18.12",
        "numpy>=1.25.2"
    ],
    python_requires=">=3.10"
)
