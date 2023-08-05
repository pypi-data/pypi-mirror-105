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
    'version': '0.3.0',
    'description': 'Simple and safe python wrapper for calling system rsync',
    'long_description': None,
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
