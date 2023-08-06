# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oslodb_sqlalchemy_exceptions']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.2.0,<2.0.0', 'debtcollector>=1.2.0,<2.0.0', 'funcsigs==1.0.2']

setup_kwargs = {
    'name': 'oslodb-sqlalchemy-exceptions',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Douglas Bett',
    'author_email': 'bettdalpha@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
