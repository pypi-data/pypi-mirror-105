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
    'version': '0.5.1',
    'description': 'Command line tool to keep logs',
    'long_description': "# `logbook-cli`\n\nCommand line tool to keep logs.\n\n**Usage**:\n\n```console\n$ logbook-cli [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `add`: Add a log entry to the logbook.\n* `delete`: Delete a log entry using it's ID.\n* `edit`: Update a log entry using it's ID.\n* `find`: List all log entries that match the argument.\n* `list`: List all log entries in a table, limits upto...\n* `view`: View a single log entry using it's ID.\n\n## `logbook-cli add`\n\nAdd a log entry to the logbook.\n\n**Usage**:\n\n```console\n$ logbook-cli add [OPTIONS] DESCRIPTION\n```\n\n**Arguments**:\n\n* `DESCRIPTION`: Description of the log entry  [required]\n\n**Options**:\n\n* `-d, --date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`: Date of the log entry  [default: **log entry date**]\n* `-t, --time [%H:%M:%S|%I:%M %p]`: Time of the log entry  [default: **log entry time**]\n* `--help`: Show this message and exit.\n\n## `logbook-cli delete`\n\nDelete a log entry using it's ID.\n\n**Usage**:\n\n```console\n$ logbook-cli delete [OPTIONS] ID\n```\n\n**Arguments**:\n\n* `ID`: ID of the log entry  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `logbook-cli edit`\n\nUpdate a log entry using it's ID.\n\n**Usage**:\n\n```console\n$ logbook-cli edit [OPTIONS] ID\n```\n\n**Arguments**:\n\n* `ID`: ID of the log entry  [required]\n\n**Options**:\n\n* `--description TEXT`: New Description for the log entry  [default: ]\n* `-d, --date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`: New Date for the log entry\n* `-t, --time [%H:%M:%S|%I:%M %p]`: New Time for the log entry\n* `--help`: Show this message and exit.\n\n## `logbook-cli find`\n\nList all log entries that match the argument.\n\n**Usage**:\n\n```console\n$ logbook-cli find [OPTIONS] DESCRIPTION_CONTAINS\n```\n\n**Arguments**:\n\n* `DESCRIPTION_CONTAINS`: String that may match log entry description  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `logbook-cli list`\n\nList all log entries in a table, limits upto 40 log entries.\n\n**Usage**:\n\n```console\n$ logbook-cli list [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `logbook-cli view`\n\nView a single log entry using it's ID.\n\n**Usage**:\n\n```console\n$ logbook-cli view [OPTIONS] ID\n```\n\n**Arguments**:\n\n* `ID`: ID of the log entry  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n",
    'author': 'Maksudul Haque',
    'author_email': 'saad.mk112@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/saadmk11/logbook-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
