# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qlikflow']

package_data = \
{'': ['*']}

install_requires = \
['requests-ntlm>=1.1.0,<2.0.0', 'requests>=2.25.1,<3.0.0', 'zeep>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'qlikflow',
    'version': '1.0.5',
    'description': 'This module allows you to create simple Apache Airflow DAG files-constructors for QlikView, Qlik Sense and NPrinting.',
    'long_description': "# qlikflow\n\n## Description\n\nThis module allows you to create simple Apache Airflow DAG files-constructors for QlikView, Qlik Sense and NPrinting.\n\n## Install\n\n``` bash\npip3 install qlikflow\n```\n\n## Create config-file\n\nOpen ``config_generator.py`` with your IDE editor, and set settings, save script\n\nThen run script to create ``config.json`` file\n\nPut this ``config.json`` file on your Apache Airflow server in folder with ``DAG``'s\n\n## Use in DAG-files\n\n``` python\nfrom airflow import DAG\nfrom airflow.utils.dates import days_ago\nimport qlikflow\nfrom datetime import datetime\n\ntasksDict = {\n    u'qliksense. Test task': {\n        'Soft' : 'qs1',\n        'TaskId' : 'c5d80e71-f574-4655-8874-3a6e2aed6218',\n        'RandomStartDelay' : 10, \n        },\n    u'np100. run nprinting tasks' : {\n        'Soft' : 'np100',\n        'TaskId' : [\n            'taskid1',\n            'taskid2',\n            'taskid3',\n            'taskid4',\n        ],\n        'Dep' : {\n            u'qliksense. Test task',\n            }\n        }\n    }\n\ndefault_args  = {\n    'owner': 'test',\n    'depends_on_past': False,\n}\n\ndag = DAG(\n    dag_id = '_my_test_dag',\n    default_args = default_args ,\n    start_date = days_ago(1),\n    schedule_interval = '@daily',\n    description = 'Default test dag',\n    tags = ['qliksense', 'testing'],\n    catchup = False\n)\n\nairflowTasksDict = {}\nqlikflow.create_tasks(tasksDict, airflowTasksDict, dag)\n```\n",
    'author': 'bintocher',
    'author_email': 'schernov1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bintocher/qlikflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
