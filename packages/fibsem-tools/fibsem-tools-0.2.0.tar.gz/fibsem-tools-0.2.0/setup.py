# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fibsem_tools', 'fibsem_tools.attrs', 'fibsem_tools.io']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0',
 'distributed>=2021.1.1,<2022.0.0',
 'fsspec>=2021.4.0,<2022.0.0',
 'h5py>=3.1.0,<4.0.0',
 'mrcfile>=1.2.0,<2.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 's3fs>=2021.4.0,<2022.0.0',
 'tensorstore>=0.1.8,<0.2.0',
 'zarr<=2.7.0']

setup_kwargs = {
    'name': 'fibsem-tools',
    'version': '0.2.0',
    'description': 'Tools for processing FIBSEM datasets',
    'long_description': None,
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
