# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wizardry', 'wizardry.catalog']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['wizardry = wizardry.cli:app']}

setup_kwargs = {
    'name': 'wizardry',
    'version': '0.1.0',
    'description': '',
    'long_description': '## What is it?\n\nWizardry is a CLI for building powerful algorithmic trading strategies faster and easier (for Lean/QuantConnect)\n\n## Installation\n\n```\npip install wizardry\n```\n',
    'author': 'ssantoshp',
    'author_email': 'santoshpassoubady@gmail.com',
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
