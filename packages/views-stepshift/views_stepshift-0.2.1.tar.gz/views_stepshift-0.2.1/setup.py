# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['views_stepshift']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.0.1,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'statsmodels>=0.12.2,<0.13.0',
 'toolz>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'views-stepshift',
    'version': '0.2.1',
    'description': 'The code used to run modelling pipelines at ViEWS',
    'long_description': '\n# ViEWS Stepshift\n\nThis package contains the modelling procedure from ViEWS2, along with helpers and auxiliary functions.\n',
    'author': 'Frederick Hoyles',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
