# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simsam']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0']

setup_kwargs = {
    'name': 'simsam',
    'version': '0.1.1',
    'description': 'Simplex sampling algorithm',
    'long_description': None,
    'author': 'Bastian Rieck',
    'author_email': 'bastian@rieck.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Pseudomanifold/Simsam',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
