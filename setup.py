#!/usr/bin/env python
import os

from setuptools import setup
setup(name='freeseer',
      version='2.5.3',
      description='video recording and streaming tool',
      author='fosslc',
      author_email='fosslc@gmail.com',
      url='http://wiki.github.com/fosslc/freeseer/',
      long_description='Freeseer is a tool for capturing or streaming video.\n\n\
It enables you to capture great presentations, demos, training material,\n\
and other videos. It handles desktop screen-casting with ease.\n\n\
Freeseer is one of a few such tools that can also record vga output \n\
or video from external sources such as firewire, usb, s-video, or rca.\n\n\
It is particularly good at handling very large conferences with hundreds \n\
of talks and speakers using varied hardware and operating systems.\n\n\
Freeseer itself can run on commodity hardware such as a laptop or desktop.',
      license='GPLv3',
      package_dir={'freeseer': 'src/freeseer'},
      packages=['freeseer', 'freeseer.backend',
                            'freeseer.framework',
                            'freeseer.frontend',
                            'freeseer.frontend.configtool',
                            'freeseer.frontend.talkeditor',
                            'freeseer.frontend.default'],
      scripts=['src/freeseer-record', 'src/freeseer-config', 'src/freeseer-talkeditor'],
      data_files=[('share/applications', ['data/freeseer.desktop']),
                  ('share/applications', ['data/48x48-freeseer.png'])]
)
