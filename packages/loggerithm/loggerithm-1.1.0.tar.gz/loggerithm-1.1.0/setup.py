# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loggerithm']

package_data = \
{'': ['*']}

install_requires = \
['coloured>=0.1,<0.2', 'toml>=0.10,<0.11']

setup_kwargs = {
    'name': 'loggerithm',
    'version': '1.1.0',
    'description': '',
    'long_description': None,
    'author': 'Totobird',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
