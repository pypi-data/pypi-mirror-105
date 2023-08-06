# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapmap_archiver', 'snapmap_archiver.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'snapmap-archiver',
    'version': '1.2.0',
    'description': 'Download all Snapmaps content from a specific location.',
    'long_description': None,
    'author': 'king-millez',
    'author_email': 'Millez.Dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
