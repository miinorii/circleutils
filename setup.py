from setuptools import setup

setup(
    name="circleutils",
    author="miinorii",
    version="2023.7.1",
    packages=["circleutils"],
    install_requires=[
        "pydantic==1.10.9",
        "numpy",
        "pandas"
    ]
)
