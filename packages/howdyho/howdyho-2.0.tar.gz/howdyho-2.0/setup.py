# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['howdyho']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'howdyho',
    'version': '2.0',
    'description': '',
    'long_description': None,
    'author': 'voronin9032',
    'author_email': 'voronin9032n3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
