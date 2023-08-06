# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cg_simulator', 'cg_simulator.accordion']

package_data = \
{'': ['*']}

install_requires = \
['dask[distributed]>=2021.4.1,<2022.0.0',
 'numba>=0.53.1,<0.54.0',
 'numpy>=1.20.2,<2.0.0',
 'rich>=10.1.0,<11.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['cgs = cg_simulator.cli:app']}

setup_kwargs = {
    'name': 'cg-simulator',
    'version': '0.1.1',
    'description': 'A simulator for card games.',
    'long_description': None,
    'author': 'Raymond DeVries',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
