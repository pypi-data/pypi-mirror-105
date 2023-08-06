# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chunin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chunin',
    'version': '0.0.1',
    'description': 'Checks Union',
    'long_description': None,
    'author': 'Oleh Mazur',
    'author_email': 'real.trolforever@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
