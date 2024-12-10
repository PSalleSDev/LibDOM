from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='LibDOM',
    version='0.1.1',
    url='https://github.com/PSalleSDev/LibDOM',
    license='MIT License',
    author='Pedro Salles',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='Html, Builder, Html Builder, DOM, Document Object Model, DOM Builder',
    description=u'LibDOM is a Python library that abstracts all modern HTML tags, enabling you to build dynamic HTML documents programmatically. With a clean and intuitive Framework, LibDOM simplifies web development by allowing you to generate and manipulate HTML entirely in Python. Perfect for creating dynamic, maintainable, and responsive web pages.',
    packages=['LibDOM'],)