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
    'version': '0.5.2',
    'description': 'Keep Your Daily Events Recorded on Your Logbook Using Command Line.',
    'long_description': '![Logbook-cli-banner](https://user-images.githubusercontent.com/24854406/118286755-9fbe4980-b4f4-11eb-8c53-1af215343e8e.png)\n\n# logbook-cli\n\nKeep Your Daily Events Recorded on Your Logbook Using Command Line.\n\n\n## How Does It Work?\n\n`logbook-cli` is created using python. It uses `typer` for the Command Line Interface\nand `SQLAlchemy` to interact with the database (`sqlite`).\nAll the log entries are stored into the `sqlite` database.\n\n\n## Installation\n\nYou can install `logbook-cli` by using `pip`:\n\n```console\npip install logbook-cli\n```\n\n\n## Configuration\n\n`logbook-cli` stores the `sqlite` database in `~/.logbook/` directory by default.\n\nYou can use `LOG_BOOK_DATABASE_URL` environment variable to use a different location.\n\n**Example:**\n\n```console\nexport LOG_BOOK_DATABASE_URL=sqlite:///logbook.sqlite3\n```\n\n\n## How to use `logbook-cli`\n\n**Usage**\n\n```console\n$ logbook-cli [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `add`: Add a log entry to the logbook.\n* `delete`: Delete a log entry using it\'s ID.\n* `edit`: Update a log entry using it\'s ID.\n* `find`: List all log entries that match the argument.\n* `list`: List all log entries in a table, limits upto...\n* `view`: View a single log entry using it\'s ID.\n\n### `logbook-cli add`\n\nAdd a log entry to the logbook.\n\n**Usage**:\n\n```console\n$ logbook-cli add [OPTIONS] DESCRIPTION\n```\n\n**Arguments**:\n\n* `DESCRIPTION`: Description of the log entry  [required]\n\n**Options**:\n\n* `-d, --date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`: Date of the log entry  [default: **log entry date**]\n* `-t, --time [%H:%M:%S|%I:%M %p]`: Time of the log entry  [default: **log entry time**]\n* `--help`: Show this message and exit.\n\n**Example:**\n\n```console\n$ logbook-cli add -d "2021-05-10" -t "10:00 PM" "This is a Test Log Entry"\n```\n\n### `logbook-cli delete`\n\nDelete a log entry using it\'s ID.\n\n**Usage**:\n\n```console\n$ logbook-cli delete [OPTIONS] ID\n```\n\n**Arguments**:\n\n* `ID`: ID of the log entry  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Example:**\n\n```console\n$ logbook-cli delete 1\n```\n\n### `logbook-cli edit`\n\nUpdate a log entry using it\'s ID.\n\n**Usage**:\n\n```console\n$ logbook-cli edit [OPTIONS] ID\n```\n\n**Arguments**:\n\n* `ID`: ID of the log entry  [required]\n\n**Options**:\n\n* `--description TEXT`: New Description for the log entry  [default: ]\n* `-d, --date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`: New Date for the log entry\n* `-t, --time [%H:%M:%S|%I:%M %p]`: New Time for the log entry\n* `--help`: Show this message and exit.\n\n**Example:**\n\n```console\n$ logbook-cli edit 1 -d "2021-05-10" -t "10:00 PM" --description "This is a Edited Test Log Entry"\n```\n\n### `logbook-cli find`\n\nList all log entries that match the argument.\n\n**Usage**:\n\n```console\n$ logbook-cli find [OPTIONS] DESCRIPTION_CONTAINS\n```\n\n**Arguments**:\n\n* `DESCRIPTION_CONTAINS`: String that may match log entry description  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Example:**\n\n```console\n$ logbook-cli find "test"\n```\n\n### `logbook-cli list`\n\nList all log entries in a table, limits upto 40 log entries.\n\n**Usage**:\n\n```console\n$ logbook-cli list [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Example:**\n\n```console\n$ logbook-cli list\n```\n\n### `logbook-cli view`\n\nView a single log entry using it\'s ID.\n\n**Usage**:\n\n```console\n$ logbook-cli view [OPTIONS] ID\n```\n\n**Arguments**:\n\n* `ID`: ID of the log entry  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Example:**\n\n```console\n$ logbook-cli view 1\n```\n\n## Screenshot\n\n![logbook-cli-screenshot](https://user-images.githubusercontent.com/24854406/118287484-4dc9f380-b4f5-11eb-8e2a-e6bf0bf35942.png)\n\n',
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
