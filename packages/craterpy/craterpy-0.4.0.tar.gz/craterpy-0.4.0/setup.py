# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['craterpy', 'craterpy.tests']

package_data = \
{'': ['*'], 'craterpy': ['data/*', 'data/_images/*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'rasterio>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'craterpy',
    'version': '0.4.0',
    'description': 'A package for impact crater data science.',
    'long_description': None,
    'author': 'Christian J. Tai Udovicic',
    'author_email': 'cj.taiudovicic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjtu/craterpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.7,<4.0.0',
}


setup(**setup_kwargs)
