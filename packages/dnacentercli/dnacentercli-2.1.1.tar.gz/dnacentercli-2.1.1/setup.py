# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dnacentercli',
 'dnacentercli.cli',
 'dnacentercli.cli.utils',
 'dnacentercli.cli.v1_2_10',
 'dnacentercli.cli.v1_3_0',
 'dnacentercli.cli.v1_3_1',
 'dnacentercli.cli.v1_3_3',
 'dnacentercli.cli.v2_1_1',
 'dnacentercli.cli.v2_1_2',
 'dnacentercli.cli.v2_2_1']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'dnacentersdk>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'dnacentercli',
    'version': '2.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jose Bogarin Solano',
    'author_email': 'jbogarin@altus.cr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
