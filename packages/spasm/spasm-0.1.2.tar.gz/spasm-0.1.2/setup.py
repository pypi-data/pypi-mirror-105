# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spasm']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'docopt>=0.6.2,<0.7.0', 'pydle>=0.9.4,<0.10.0']

entry_points = \
{'console_scripts': ['spasm = spasm:main']}

setup_kwargs = {
    'name': 'spasm',
    'version': '0.1.2',
    'description': 'A simple twitch.tv chat viewer.',
    'long_description': '',
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
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
