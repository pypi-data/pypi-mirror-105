# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flashbots']

package_data = \
{'': ['*']}

install_requires = \
['web3>=5.17.0,<5.18.0']

setup_kwargs = {
    'name': 'flashbots',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Georgios Konstantopoulos',
    'author_email': 'me@gakonst.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
