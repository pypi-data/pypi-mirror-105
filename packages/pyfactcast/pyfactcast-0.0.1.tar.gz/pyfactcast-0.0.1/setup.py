# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfactcast']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.37.1,<2.0.0']

setup_kwargs = {
    'name': 'pyfactcast',
    'version': '0.0.1',
    'description': 'A python client library for FactCast',
    'long_description': None,
    'author': 'Eduard Thamm',
    'author_email': 'eduard.thamm@thammit.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
