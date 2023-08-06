# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nicegui', 'nicegui.elements']

package_data = \
{'': ['*']}

install_requires = \
['icecream>=2.1.0,<3.0.0',
 'justpy==0.1.5',
 'matplotlib>=3.4.1,<4.0.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'nicegui',
    'version': '0.1.4',
    'description': 'High-Level Abstraction Web-GUI Using Just Python',
    'long_description': None,
    'author': 'Zauberzeug GmbH',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
