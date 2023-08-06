# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jittoku', 'jittoku.cli']

package_data = \
{'': ['*']}

install_requires = \
['ase>=3.21.1,<4.0.0']

entry_points = \
{'jittoku.commands': ['entries2json = jittoku.cli.entries2json:main',
                      'json2entries = jittoku.cli.json2entries:main']}

setup_kwargs = {
    'name': 'jittoku',
    'version': '0.1.0',
    'description': 'Useful scripts for QE etc.',
    'long_description': None,
    'author': 'Koki Muraoka',
    'author_email': 'koki.muraoka@gmail.com',
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
