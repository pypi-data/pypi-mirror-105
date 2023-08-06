# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpymc3']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jrpymc3',
    'version': '0.1.1',
    'description': 'Jumping Rivers: Bayesian Inference with PyMC3',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
