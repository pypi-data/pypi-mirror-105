# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entropylab_qpudb']

package_data = \
{'': ['*']}

install_requires = \
['ZODB>=5.6.0,<6.0.0', 'pandas>=1.2.4,<2.0.0']

setup_kwargs = {
    'name': 'entropylab-qpudb',
    'version': '0.0.4',
    'description': 'A extension of entropy lab for persistent storage of calibration parameters of a quantum processing unit (QPU)',
    'long_description': '# QPU DB Entropy extension\n\nThe QPU DB is a specialized interface used to access parameters and calibrations\nthat are tracked between quantum experiments and enable detection of staleness\nEntropy\n\nThe QPU DB is an extension of entropylab package.',
    'author': 'Lior Ella',
    'author_email': 'lior@quantum-machines.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/entropy-lab/entropy-qpu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
