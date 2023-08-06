# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygharar']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pygharar',
    'version': '0.0.2',
    'description': 'Gharar client in python',
    'long_description': '# Gharar Python Client\n\nThis is a python adaptor for interact with \n[Gharar](https://http://gharar.ir) service.\n\n# Installation\n\nYou can easily install the package via command line below:\n\n```commandline\npip install pygharar\n```\n\n# Usage\n\n```python\nfrom pygharar import Gharar\n\nmy_gharar = Gharar(\n    service_url="https://gharar.ir/",\n    authorization_token="PUT YOUR OWN TOKEN HERE", \n    max_retry=3\n)\n```\n',
    'author': 'Yazdan Ranjbar',
    'author_email': 'Yazdan_ra@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
