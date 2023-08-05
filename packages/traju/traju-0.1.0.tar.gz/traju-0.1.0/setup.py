# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traju']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['traju = traju.cli:main']}

setup_kwargs = {
    'name': 'traju',
    'version': '0.1.0',
    'description': 'traju makes manipulation with MD trajectories using AmberTools a little bit easier',
    'long_description': '# traju\n\n`traju` makes manipulation with MD trajectories using AmberTools a little bit easier.\n\n\n* Free software: MIT license\n\n\n## Features\n\n* TODO',
    'author': 'Vsevolod O. Shegolev',
    'author_email': 'v.sheg@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vsheg/traju',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
