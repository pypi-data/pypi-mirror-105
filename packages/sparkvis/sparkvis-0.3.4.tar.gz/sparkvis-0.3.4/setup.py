# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sparkvis']

package_data = \
{'': ['*']}

install_requires = \
['sparklines>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'sparkvis',
    'version': '0.3.4',
    'description': 'Visualize tensors using Sparklines',
    'long_description': None,
    'author': 'Shawn Presser',
    'author_email': 'shawnpresser@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
