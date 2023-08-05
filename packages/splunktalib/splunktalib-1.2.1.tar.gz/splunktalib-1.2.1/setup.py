# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splunktalib',
 'splunktalib.common',
 'splunktalib.concurrent',
 'splunktalib.conf_manager',
 'splunktalib.schedule']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0', 'httplib2==0.19.1', 'sortedcontainers>=2.2,<3.0']

setup_kwargs = {
    'name': 'splunktalib',
    'version': '1.2.1',
    'description': 'Supporting library for Splunk Add-ons',
    'long_description': None,
    'author': 'rfaircloth-splunk',
    'author_email': 'rfaircloth@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/splunk/addonfactory-ta-library-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
