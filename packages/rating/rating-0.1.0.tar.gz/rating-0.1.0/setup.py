# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rating']

package_data = \
{'': ['*'], 'rating': ['backends/*']}

setup_kwargs = {
    'name': 'rating',
    'version': '0.1.0',
    'description': 'Ratings made easy',
    'long_description': None,
    'author': 'tba91',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
