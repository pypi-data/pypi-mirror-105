# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['impm', 'impm.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'colorlog>=4.2.1,<5.0.0']

setup_kwargs = {
    'name': 'impm',
    'version': '0.1.0',
    'description': 'Python utilities for improving interoperability between Minecraft data packs.',
    'long_description': '# impm\n\nPython utilities for improving interoperability between Minecraft data packs.\n',
    'author': 'Arcensoth',
    'author_email': 'arcensoth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arcensoth/impm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
