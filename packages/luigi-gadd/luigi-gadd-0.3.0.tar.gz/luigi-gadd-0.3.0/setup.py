# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['luigi_gadd']

package_data = \
{'': ['*']}

install_requires = \
['luigi>=3.0,<4.0']

setup_kwargs = {
    'name': 'luigi-gadd',
    'version': '0.3.0',
    'description': 'Provides additional functionality to make Luigi more flexible',
    'long_description': None,
    'author': 'Mike Lynch',
    'author_email': 'me@msl.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mikelynch/luigi-gadd',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
