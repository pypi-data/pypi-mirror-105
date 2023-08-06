# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['app_typer']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['app-typer = app_typer.main:app']}

setup_kwargs = {
    'name': 'app-typer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ysd',
    'author_email': 'helloysd@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
