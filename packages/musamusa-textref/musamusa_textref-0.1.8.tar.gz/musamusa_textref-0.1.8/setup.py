# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['musamusa_textref']

package_data = \
{'': ['*']}

install_requires = \
['musamusa-errors>=0.8,<0.9', 'musamusa-romannumbers>=0.0.8,<0.0.9']

setup_kwargs = {
    'name': 'musamusa-textref',
    'version': '0.1.8',
    'description': '"Beowulf.4c" < "Beowulf.5a"',
    'long_description': None,
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
