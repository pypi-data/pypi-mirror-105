# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['versionizer']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.15,<4.0.0',
 'asciistuff>=1.2.2,<2.0.0',
 'astor>=0.8.1,<0.9.0',
 'pynguin>=0.8.0,<0.9.0',
 'pytest>=6.2.4,<7.0.0']

setup_kwargs = {
    'name': 'versionizer',
    'version': '0.1.0',
    'description': 'Versionizer is a tool for automatically generating unit tests for functions that change between two commits.',
    'long_description': None,
    'author': 'Jordan Gillard',
    'author_email': 'jordan-gillard@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
