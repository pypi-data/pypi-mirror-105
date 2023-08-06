from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

version = {}
ver_text = (here / 'tealight' / 'version.py').read_text(encoding='utf-8')
exec(ver_text, version)

req_file = here / 'requirements.txt'
requirements = req_file.read_text().splitlines()

setup(
    name='tealight',
    version=version['__version__'],
    description=(
        'A very small candlestick library'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/asongtoruin/tealight',
    author='Adam Ruszkowski',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=requirements,
    project_urls={
        'Source': 'https://github.com/asongtoruin/tealight/',
    },
)