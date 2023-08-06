# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sysrsync', 'sysrsync.helpers']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'sysrsync',
    'version': '0.3.1',
    'description': 'Simple and safe python wrapper for calling system rsync',
    'long_description': "# sysrsync\nSimple and safe native rsync wrapper for Python 3\n\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=gchamon_sysrsync&metric=alert_status)](https://sonarcloud.io/dashboard?id=gchamon_sysrsync)\n\n## Requirements\n\n* rsync\n* python 3.6+\n\n**development**:\n\n* poetry (be sure to have both poetry and pip upgraded to the latest version)\n\n## Installation\n\n`pip install sysrsync`\n\n## Basic rules\n\n- Syncs source contents by default, so it adds a trailing slash to the end of source, unless `sync_source_contents=False` is specified\n- Removes trailing slash from destination\n- Extra arguments are put right after `rsync`\n- Breaks if `source_ssh` and `destination_ssh` are both set\n\n## Usage\n\n* Basic file sync\n\n```python\nimport sysrsync\n\nsysrsync.run(source='/home/user/foo.txt',\n             destination='/home/server/bar')\n# runs 'rsync /home/users/foo.txt /home/server/files'\n```\n\n* sync whole folder\n\n```python\nimport sysrsync\n\nsysrsync.run(source='/home/user/files',\n             destination='/home/server/',\n             sync_source_contents=False)\n# runs 'rsync /home/user/files /home/server'\n```\n\n* sync folder contents\n\n```python\nimport sysrsync\n\nsysrsync.run(source='/home/user/files',\n             destination='/home/server/',\n             sync_source_contents=True)\n# runs 'rsync /home/user/files/ /home/server'\n```\n\n* ssh with options\n\n```python\nimport sysrsync\n\nsysrsync.run(source='/home/user/files',\n             destination='/home/server/files',\n             destination_ssh='myserver',\n             options=['-a'])\n# runs 'rsync -a /home/users/files/ myserver:/home/server/files'\n```\n\n* exclusions\n\n```python\nimport sysrsync\n\nsysrsync.run(source='/home/user/files',\n             destination='/home/server/files',\n             destination_ssh='myserver',\n             options=['-a'],\n             exclusions=['file_to_exclude', 'unwanted_file'])\n# runs 'rsync -a /home/users/files/ myserver:/home/server/files --exclude file_to_exclude --exclude unwanted_file'\n```\n\n## API\n\n`sysrsync.run`\n\n| argument  | type | default | description |\n| --------- | ---- | ------- | ----------- |\n| cwd  | str  | `os.getcwd()` | working directory in which subprocess will run the rsync command |\n| strict  | bool | `True` | raises `RsyncError` when rsync return code is different than 0  |\n| verbose | bool | `False` | verbose mode: currently prints rsync command before executing |\n| **kwargs | dict | Not Applicable | arguments that will be forwarded to call to `sysrsync.get_rsync_command` |\n\n**returns**: `subprocess.CompletedProcess`\n\n**raises**: `RsyncError` when `strict = True` and rsync return code is different than 0 ([Success](https://lxadm.com/Rsync_exit_codes#List_of_standard_rsync_exit_codes))\n\n`sysrsync.get_rsync_command`\n\n| argument  | type | default | description |\n| --------- | ---- | ------- | ----------- |\n| source | str | - | Source folder or file |\n| destination | str | - | Destination folder |\n| source_ssh | Optional[str] | None | Remote ssh client where source is located |\n| destination_ssh | Optional[str] | None | Remote ssh client where destination is located |\n| exclusions | Iterable[str] | [] | List of excluded patterns as in rsync's `--exclude` |\n| sync_source_contents | bool | True | Abstracts the elusive trailing slash behaviour that `source` normally has when using rsync directly, i.e. when a trailing slash is present in `source`, the folder's content is synchronized with destination. When no trailing slash is present, the folder itself is synchronized with destination. |\n| options | Iterable[str] | [] | List of options to be used right after rsync call, e.g. `['-a', '-v']` translates to `rsync -a -v` |\n\n**returns**: `List[str]` -> the compiled list of commands to be used directly in `subprocess.run`\n\n**raises**: `RemotesError` when both `source_ssh` and `destination_ssh` are set. Normally linux rsync distribution disallows source and destination to be both remotes.\n",
    'author': 'Gabriel Chamon',
    'author_email': 'gchamon@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
