# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qlikflow']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'qlikflow',
    'version': '1.0.0',
    'description': 'This module allows you to create simple Apache Airflow DAG files-constructors for QlikView, Qlik Sense and NPrinting.',
    'long_description': None,
    'author': 'bintocher',
    'author_email': 'schernov1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
