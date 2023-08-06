# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['i3_swallow']

package_data = \
{'': ['*']}

install_requires = \
['i3ipc>=2.2.1,<3.0.0']

entry_points = \
{'console_scripts': ['swallow = i3_swallow:main']}

setup_kwargs = {
    'name': 'i3-swallow',
    'version': '0.1.0',
    'description': 'Swallow a terminal window in i3/sway',
    'long_description': None,
    'author': 'jamesofarrell',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
