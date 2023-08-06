# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['package_list']

package_data = \
{'': ['*']}

install_requires = \
['stdlib-list>=0.8.0,<0.9.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['package-list = package_list.main:app']}

setup_kwargs = {
    'name': 'package-list',
    'version': '0.2.1',
    'description': 'An awesome package is coming soon! 🎉',
    'long_description': '<h1 align="center">\n    <strong>package-list</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/package-list" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/package-list" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/package-list/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/package-list">\n    <br />\n    <a href="https://pypi.org/project/package-list" target="_blank">\n        <img src="https://img.shields.io/pypi/v/package-list" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/package-list">\n    <img src="https://img.shields.io/github/license/Kludex/package-list">\n</p>\n\n\n## Installation\n\n``` bash\npip install package-list\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/package-list',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
