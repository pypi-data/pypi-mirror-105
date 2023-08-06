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
    'version': '1.0.0',
    'description': 'Swallow a terminal window in i3/sway',
    'long_description': '<h1 align="center">\n  Swallow\n</h1>\n<h4 align="center">Used to swallow (send to the scratchpad) a terminal window after a blocking application is run in i3 window manager</h4>\n\n<p align="center">\n  <img src="https://img.shields.io/badge/Maintained%3F-Yes-green?style=for-the-badge">\n  <img src="https://img.shields.io/github/license/jamesofarrell/i3-swallow?style=for-the-badge">\n  <img src="https://img.shields.io/github/issues/jamesofarrell/i3-swallow?color=violet&style=for-the-badge">\n  <img src="https://img.shields.io/github/stars/jamesofarrell/i3-swallow?style=for-the-badge">\n  <img src="https://img.shields.io/github/forks/jamesofarrell/i3-swallow?color=teal&style=for-the-badge">\n  <img src="https://github.com/jamesofarrell/i3-swallow/blob/master/Swallow.gif">\n</p>\n\n## Information\n\nThis repo just packages [jamesofarrell/i3-swallow](https://github.com/jamesofarrell/i3-swallow) script using [Poetry](https://python-poetry.org/)\nso it can be install using `pip`\n\n## Requirements\n\n- Unix system with i3 window manager, or i3 compatible window manager such as sway\n- Python3.x+\n- Python3.x+ Pip\n\n## Installation Instruction\n\n```bash\npip install --user i3-swallow\n```\n\n## Usage\n\n```bash\nswallow -h\n```\n\n## License\n\nThis Project is licensed under the MIT License. Check license file for more info.\n',
    'author': 'jamesofarrell',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ViliamV/i3-swallow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
