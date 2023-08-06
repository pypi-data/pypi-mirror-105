# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latticeadaptor',
 'latticeadaptor.lark',
 'latticeadaptor.mappings',
 'latticeadaptor.parsers',
 'latticeadaptor.utils']

package_data = \
{'': ['*']}

install_requires = \
['lark>=0.11.3,<0.12.0',
 'matplotlib>=3.4.1,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'latticeadaptor',
    'version': '0.1.0',
    'description': '<Enter a one-sentence description of this project here.>',
    'long_description': '==============\nlatticeadaptor\n==============\n\n\n\nThis package is used to convert a table of accelerator lattice elements and their arguments \nto various accelerator lattice formats. Currently covered are:\n\n- MadX (Sequence and Line format)\n- Elegant\n- Tracy\n\n* Free software: MIT license\n* Documentation: https://latticeadaptor.readthedocs.io.\n\n\nFeatures\n--------\n\n* Fast lattice comparison by plotting element locations against eachother.\n* Fast settings compare by comparing magnet settings.\n* Quick twiss plotting.\n* Quick lattice element plotting.\n* Conversion from table to standard formats.\n',
    'author': 'Tom Mertens',
    'author_email': 'your.email@whatev.er',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomerten/latticeadaptor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
