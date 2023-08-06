# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitlab_ps_utils']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.3,<7.0.0', 'requests>=2.25.1,<3.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'gitlab-ps-utils',
    'version': '0.1.1',
    'description': 'Shared python utilities used by GitLab Professional Services tooling',
    'long_description': None,
    'author': 'GitLab Professional Services',
    'author_email': 'proserv@gitlab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
