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
    'version': '1.1.1',
    'description': 'Logging module for the Python programming language',
    'long_description': '# Python Loggerithm\nLogging module for the Python programming language\n\n## Getting Started\n1. [Creating Loggers](https://github.com/toto-bird/python-loggerithm/blob/master/examples/creating_loggers.py)\n2. [Basic Logging](https://github.com/toto-bird/python-loggerithm/blob/master/examples/basic_logging.py)\n3. [Loading Loggers From Config](https://github.com/toto-bird/python-loggerithm/blob/master/examples/load_from_config.py)\n',
    'author': 'Totobird',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/toto-bird/python-loggerithm/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
