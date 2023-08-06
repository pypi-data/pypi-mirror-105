# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kupala']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kupala',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'alex.oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
