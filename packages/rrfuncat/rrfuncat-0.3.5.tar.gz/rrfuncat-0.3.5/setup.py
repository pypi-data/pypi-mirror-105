# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrfuncat', 'rrfuncat.data']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['rrfuncat = rrfuncat.cmds:cli']}

setup_kwargs = {
    'name': 'rrfuncat',
    'version': '0.3.5',
    'description': 'rrFuncat 将同花顺、通达信、文华财经等的公式移植到了 Python 中',
    'long_description': None,
    'author': 'romepeng',
    'author_email': 'romepeng@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
