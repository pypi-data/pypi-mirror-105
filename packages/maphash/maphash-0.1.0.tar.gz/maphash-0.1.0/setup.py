# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maphash']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'maphash',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jakob Klepp',
    'author_email': 'jakob.klepp@moonvision.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
