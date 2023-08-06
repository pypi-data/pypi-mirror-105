# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhustler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyhustler',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'ashdaily',
    'author_email': 'ashtokyo31@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
