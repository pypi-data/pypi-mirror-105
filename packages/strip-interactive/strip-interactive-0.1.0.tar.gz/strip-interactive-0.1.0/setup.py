# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strip_interactive']

package_data = \
{'': ['*'], 'strip_interactive': ['.git/*', '.git/hooks/*', '.git/info/*']}

setup_kwargs = {
    'name': 'strip-interactive',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'khuyentran1401',
    'author_email': 'khuyentran1476@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
