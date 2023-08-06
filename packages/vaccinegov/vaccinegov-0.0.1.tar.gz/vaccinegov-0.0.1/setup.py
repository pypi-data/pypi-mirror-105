# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vaccinegov', 'vaccinegov.schemas']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.1.0,<2.0.0', 'httpx>=0.18.1,<0.19.0', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'vaccinegov',
    'version': '0.0.1',
    'description': "A library to interact with the U.S Government's COVID-19 Vaccine Finder tool",
    'long_description': None,
    'author': 'Mustafa',
    'author_email': 'mustafa@ms7m.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
