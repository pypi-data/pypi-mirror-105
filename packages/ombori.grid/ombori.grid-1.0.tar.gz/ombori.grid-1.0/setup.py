from setuptools import setup, find_packages

setup(
    name='ombori.grid',
    version='1.0',
    packages=find_packages(),
    install_requires=["paho-mqtt"]
)
