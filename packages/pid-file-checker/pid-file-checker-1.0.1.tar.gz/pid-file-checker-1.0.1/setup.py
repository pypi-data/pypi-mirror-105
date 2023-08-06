# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pid_file_checker']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.8.0']

entry_points = \
{'console_scripts': ['pfc = pid_file_checker.checker:main']}

setup_kwargs = {
    'name': 'pid-file-checker',
    'version': '1.0.1',
    'description': 'Monitor a pid file',
    'long_description': '# pid-file-checker\n\n```\n$ pfc --help\nusage: pfc [-h] pid_file\n\nCheck for the presence of a pid file. The file must contain one and only one\ninteger which must be the pid of a running process. Otherwise, return a code\n!= 0. Meant to be used in a healthcheck context like with Docker or\nKubernetes.\n\npositional arguments:\n  pid_file    The pid file you want to monitor\n\noptional arguments:\n  -h, --help  show this help message and exit\n\nBrought to you by IT4NW@ITSF.\n```\n',
    'author': 'Gabriel Augendre',
    'author_email': 'gabriel.augendre@itsfactory.fr',
    'maintainer': 'Gabriel Augendre',
    'maintainer_email': 'gabriel.augendre@itsfactory.fr',
    'url': 'https://github.com/itsolutionsfactory/pid-file-checker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
