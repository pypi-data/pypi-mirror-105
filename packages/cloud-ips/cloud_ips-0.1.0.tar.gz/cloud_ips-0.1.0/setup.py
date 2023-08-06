# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloud_ips']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'cloud-ips',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alexander Myasoedov',
    'author_email': 'msoedov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
