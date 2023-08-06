# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['guardian']

package_data = \
{'': ['*']}

install_requires = \
['jwt>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'kingdom-guardian',
    'version': '0.0.1.dev2',
    'description': 'Simple but safe authorization and authentication facilities',
    'long_description': '# guardian \nSimple but safe authorization and authentication facilities.\n\n## Features\n\n1. JWT for authentication\n2. AERBAC for authorization\n  - Attributes enhanced role-based access control model, i.e. RBAC w/ steroids\n\n## Usage\n\n```shell\npip install kingdom-guardian\n```\n\n```python\nfrom guardian import flow\n```\n',
    'author': 'Rui Conti',
    'author_email': 'rui@t10.digital',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/t10d/guardian',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
