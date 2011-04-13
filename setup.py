#!/usr/bin/env python

from distutils.core import setup
setup(name='freeseer',
      version='2.0.1',
      description='video studio in a backpack',
      author='fosslc',
      author_email='fosslc@gmail.com',
      url='http://wiki.github.com/fosslc/freeseer/',
      license='GPLv3',
      packages=['freeseer', 'freeseer.backend',
                            'freeseer.framework',
                            'freeseer.frontend',
                            'freeseer.frontend.configtool',
                            'freeseer.frontend.talkeditor',
                            'freeseer.frontend.default'],
      package_dir={'freeseer': 'src/freeseer'},
      )
