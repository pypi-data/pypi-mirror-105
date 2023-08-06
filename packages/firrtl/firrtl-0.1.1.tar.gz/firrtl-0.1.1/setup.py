# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['firrtl', 'firrtl.tests']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=3.17.0,<4.0.0']

setup_kwargs = {
    'name': 'firrtl',
    'version': '0.1.1',
    'description': 'Python Bindings for FIRRTL',
    'long_description': None,
    'author': 'Dan Fritchman',
    'author_email': 'dan@fritch.mn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
