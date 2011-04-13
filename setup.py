#!/usr/bin/env python

import shutil
import tempfile

# copy startup scripts to be installed
scriptdir = tempfile.mkdtemp('scripts')
shutil.copyfile('src/run-freeseer', '%s/freeseer' % scriptdir)
shutil.copyfile('src/run-configtool', '%s/freeseer-configtool' % scriptdir)
shutil.copyfile('src/run-talkeditor', '%s/freeseer-talkeditor' % scriptdir)

from setuptools import setup
setup(name='freeseer',
      version='2.0.1',
      description='video studio in a backpack',
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
      scripts=['%s/freeseer' % scriptdir, '%s/freeseer-configtool' % scriptdir, '%s/freeseer-talkeditor' % scriptdir]
      )

# cleanup
shutil.rmtree(scriptdir)

