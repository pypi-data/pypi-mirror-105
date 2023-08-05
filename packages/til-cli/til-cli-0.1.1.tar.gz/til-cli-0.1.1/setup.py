# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['til', 'til.plugins']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'ruamel.yaml>=0.17.4,<0.18.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['til = til.main:til']}

setup_kwargs = {
    'name': 'til-cli',
    'version': '0.1.1',
    'description': 'Keep track of things you learn each day',
    'long_description': None,
    'author': 'Kamyar Ghasemlou',
    'author_email': 'github@kamy.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
