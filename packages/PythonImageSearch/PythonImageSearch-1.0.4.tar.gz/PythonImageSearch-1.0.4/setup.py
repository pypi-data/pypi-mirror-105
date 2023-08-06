from setuptools import setup

setup(
    name='PythonImageSearch',
    version="1.0.4",
    url='https://github.com/RandomPythonProgrammer/python-image-search',
    author='RandomPythonProgrammer',
    author_email="jhc3628@gmail.com",
    description='Simple image search',
    long_description="Idk just a random python image search thing, it uses selenium and stuff.",
    install_requires=['selenium', 'bs4', 'requests'],
    keywords="Image Search",
    packages=["Image_Search"]
)
