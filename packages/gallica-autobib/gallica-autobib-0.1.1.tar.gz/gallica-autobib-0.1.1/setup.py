# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gallica_autobib', 'gallica_autobib.gallipy']

package_data = \
{'': ['*'], 'gallica_autobib': ['templates/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'Pillow>=8.2.0,<9.0.0',
 'PyPDF4>=1.27.0,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'bibtexparser>=1.2.0,<2.0.0',
 'fuzzysearch>=0.7.3,<0.8.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'lark-parser>=0.11.3,<0.12.0',
 'lxml>=4.6.3,<5.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'python-slugify>=5.0.2,<6.0.0',
 'requests-downloader>=0.1.6,<0.2.0',
 'rfc3987>=1.3.8,<2.0.0',
 'rispy>=0.6.0,<0.7.0',
 'roman>=3.3,<4.0',
 'scikit-image>=0.18.1,<0.19.0',
 'sruthi>=0.1.2,<0.2.0',
 'typer>=0.3.2,<0.4.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'gallica-autobib',
    'version': '0.1.1',
    'description': 'Tools to convert SQLAlchemy models to Pydantic models',
    'long_description': '# pygallica-autobib\n\n<p align="center">\n    <em>Automatically match Bibliographies against bnf.gallica.fr!</em>\n</p>\n\n<p align="center">\n<a href="https://github.com/2e0byo/pygallica-autobib/actions?query=workflow%3ATest" target="_blank">\n    <img src="https://github.com/2e0byo/pygallica-autobib/workflows/Test/badge.svg" alt="Test">\n</a>\n<a href="https://github.com/2e0byo/pygallica-autobib/actions?query=workflow%3APublish" target="_blank">\n    <img src="https://github.com/2e0byo/pygallica-autobib/workflows/Publish/badge.svg" alt="Publish">\n</a>\n<a href="https://dependabot.com/" target="_blank">\n    <img src="https://flat.badgen.net/dependabot/2e0byo/pygallica-autobib?icon=dependabot" alt="Dependabot Enabled">\n</a>\n<a href="https://codecov.io/gh/2e0byo/pygallica-autobib" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/2e0byo/pygallica-autobib?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/gallica-autobib" target="_blank">\n    <img src="https://img.shields.io/pypi/v/gallica-autobib?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/gallica-autobib/" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/gallica-autobib.svg" alt="Python Versions">\n</a>\n\n## The Basic Idea\npygallica-autobib will match your bibliographies against the French National Library and download articles as pdfs if possible, optionally post-processing them.\n\n\n## Installing gallica-autobib\n\nInstall the latest release:\n\n```bash\npip install gallica-autobib\n```\n\nOr you can clone `gallica-autobib` and get started locally\n\n```bash\n\n# ensure you have Poetry installed\npip install --user poetry\n\n# install all dependencies (including dev)\npoetry install\n\n# develop!\n\n```\n\n## Example Usage\n\n```python\nimport gallica_autobib\n\n# do stuff\n```\n',
    'author': 'John Morris',
    'author_email': '2e0byo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
