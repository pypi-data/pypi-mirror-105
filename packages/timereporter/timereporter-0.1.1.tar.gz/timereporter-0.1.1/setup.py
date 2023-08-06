# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timereporter', 'timereporter.commands', 'timereporter.views']

package_data = \
{'': ['*']}

install_requires = \
['camel>=0.1.2', 'colorama>=0.4.1', 'tabulate>=0.7.7']

setup_kwargs = {
    'name': 'timereporter',
    'version': '0.1.1',
    'description': 'Report working time from the command line.',
    'long_description': None,
    'author': 'Filip Lange',
    'author_email': 'filip.lange@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Godsmith/timereporter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
