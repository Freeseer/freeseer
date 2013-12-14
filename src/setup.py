#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

import freeseer


setup(name=freeseer.NAME,
      version=freeseer.__version__,
      author=freeseer.__author__,
      author_email=freeseer.__email__,
      url=freeseer.URL,
      description=freeseer.DESCRIPTION,
      long_description=freeseer.LONG_DESCRIPTION,
      license='GPLv3',
      classifiers = [
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Other Audience',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Microsoft :: Windows :: Windows XP',
          'Operating System :: Microsoft :: Windows :: Windows 7',
          'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
          'Topic :: Multimedia :: Video :: Capture',
          ],
      package_data={'freeseer': ['plugins/*/*/*']},
      packages=find_packages(exclude=[
          '*.tests',
          '*.tests.*',
          'tests.*',
          'tests'
          ]),
      data_files=[
          ('share/applications', ['data/freeseer.desktop']),
          ('share/applications', ['data/48x48-freeseer.png'])
          ],
      entry_points={
        'console_scripts': [
            'freeseer = freeseer:main',
          ],
        },
      test_suite='freeseer.tests'
      )
