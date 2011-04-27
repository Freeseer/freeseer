#!/usr/bin/env python

import shutil
import tempfile

from setuptools import setup
setup(name='freeseer',
      version='2.5.2',
      description='video recording and streaming tool',
      author='fosslc',
      author_email='fosslc@gmail.com',
      url='http://wiki.github.com/fosslc/freeseer/',
      license='GPLv3',
      package_dir={'freeseer': 'src/freeseer'},
      packages=['freeseer', 'freeseer.backend',
                            'freeseer.framework',
                            'freeseer.frontend',
                            'freeseer.frontend.configtool',
                            'freeseer.frontend.talkeditor',
                            'freeseer.frontend.default'],
      scripts=['src/freeseer-record', 'src/freeseer-config', 'src/freeseer-talkeditor'])

