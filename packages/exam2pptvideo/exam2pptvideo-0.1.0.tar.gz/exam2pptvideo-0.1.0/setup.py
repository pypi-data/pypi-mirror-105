# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exam2pptvideo', 'exam2pptvideo._entry', 'exam2pptvideo.es']

package_data = \
{'': ['*'], 'exam2pptvideo.es': ['soundaffects/*', 'templates/*']}

install_requires = \
['click>=8.0.0,<9.0.0',
 'pdf2image>=1.15.1,<2.0.0',
 'python-pptx>=0.6.18,<0.7.0']

entry_points = \
{'console_scripts': ['exam_csv2pptx = exam2pptvideo._entry.command:csv2pptx',
                     'exam_pptx2media = '
                     'exam2pptvideo._entry.command:pptx2pdf2images',
                     'exam_pptx2video = '
                     'exam2pptvideo._entry.command:pptx2video',
                     'exam_pptx_validate = '
                     'exam2pptvideo._entry.validation:validate']}

setup_kwargs = {
    'name': 'exam2pptvideo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
