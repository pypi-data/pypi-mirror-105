# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logbook_cli']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.4.15',
 'colorama==0.4.4',
 'shellingham==1.4.0',
 'tabulate==0.8.9',
 'typer==0.3.2']

entry_points = \
{'console_scripts': ['logbook-cli = logbook_cli.cli:app']}

setup_kwargs = {
    'name': 'logbook-cli',
    'version': '0.5.0',
    'description': 'Command line tool to keep logs',
    'long_description': '# logbook-cli\n',
    'author': 'Maksudul Haque',
    'author_email': 'saad.mk112@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
