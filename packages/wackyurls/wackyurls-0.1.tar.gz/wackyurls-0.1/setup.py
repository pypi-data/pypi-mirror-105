import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / 'readme.md').read_text()

setup(
    name='wackyurls',
    packages=['wackyurls'],
    version='0.1',
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    author='briccardo',
    author_email='rbiagini02@gmail.com',
    description='Generates random URLs from nouns and adjectives.',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True
)
