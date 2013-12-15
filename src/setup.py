#!/usr/bin/env python
import os

from setuptools import setup

from freeseer import __version__, NAME, __author__, __email__, URL, DESCRIPTION

setup(name=NAME,
      version=__version__,
      author=__author__,
      author_email=__email__,
      url=URL,
      description=DESCRIPTION,
      long_description='Freeseer is a tool for capturing or streaming video.\n\n\
It enables you to capture great presentations, demos, training material,\n\
and other videos. It handles desktop screen-casting with ease.\n\n\
Freeseer is one of a few such tools that can also record vga output \n\
or video from external sources such as firewire, usb, s-video, or rca.\n\n\
It is particularly good at handling very large conferences with hundreds \n\
of talks and speakers using varied hardware and operating systems.\n\n\
Freeseer itself can run on commodity hardware such as a laptop or desktop.',
      license='GPLv3',
      classifiers = [
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Development Status :: 4 - Beta",
          "Intended Audience :: Education",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: Information Technology",
          "Intended Audience :: Other Audience",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: POSIX :: Linux",
          "Operating System :: Microsoft :: Windows :: Windows XP",
          "Operating System :: Microsoft :: Windows :: Windows 7",
          "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
          "Topic :: Multimedia :: Video :: Capture",
          ],
      package_data={'freeseer': ['plugins/*/*/*', 'plugins/*/*.freeseer-plugin']},
      packages=['freeseer', 'freeseer.framework',
                            'freeseer.frontend',
                            'freeseer.frontend.configtool',
                            'freeseer.frontend.controller',
                            'freeseer.frontend.qtcommon',
                            'freeseer.frontend.reporteditor',
                            'freeseer.frontend.talkeditor',
                            'freeseer.frontend.record'],
      data_files=[('share/applications', ['data/freeseer.desktop']),
                  ('share/applications', ['data/48x48-freeseer.png'])],
      scripts=['freeseer-record', 'freeseer-config', 'freeseer-talkeditor',
               'freeseer-reporteditor'],
      test_suite='freeseer.tests')

