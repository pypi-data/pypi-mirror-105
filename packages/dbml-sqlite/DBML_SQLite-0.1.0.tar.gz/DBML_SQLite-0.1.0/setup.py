# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbml_sqlite']

package_data = \
{'': ['*']}

install_requires = \
['pydbml>=0.3.4,<0.4.0']

setup_kwargs = {
    'name': 'dbml-sqlite',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dave VanderWeele',
    'author_email': 'weele.me@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
