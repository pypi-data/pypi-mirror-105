import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='ventaapi',
    packages=find_packages(include=['ventaapi']),
    install_requires=['asyncio', 'aiohttp'],
    version='1.0.0',
    description='Local API connector library for Venta Air Washers',
    author='Vladislav Sharapov',
    license='MIT',
    long_description=README,
    long_description_content_type="text/markdown",
)
