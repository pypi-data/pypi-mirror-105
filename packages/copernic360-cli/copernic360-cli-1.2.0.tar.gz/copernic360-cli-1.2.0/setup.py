# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['copernic360_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'click>=7.1.2,<8.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['copernic360 = copernic360_cli.__main__:cli']}

setup_kwargs = {
    'name': 'copernic360-cli',
    'version': '1.2.0',
    'description': "Command-line script for Kagenova's Copernic360 API",
    'long_description': None,
    'author': 'Kagenova',
    'author_email': None,
    'maintainer': "Mayeul d'Avezac",
    'maintainer_email': 'mayeul.davezac@kagenova.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
