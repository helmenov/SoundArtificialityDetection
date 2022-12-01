# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soundartificialitydetection']

package_data = \
{'': ['*']}

install_requires = \
['SoundFile>=0.10.3,<0.11.0',
 'japanize-matplotlib>=1.1.3,<2.0.0',
 'librosa>=0.9.2,<0.10.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'soundartificialitydetection',
    'version': '0.2.1',
    'description': '',
    'long_description': 'None',
    'author': 'Kotaro SONODA',
    'author_email': 'kotaro1976@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
