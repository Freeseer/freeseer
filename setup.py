from distutils.core import setup
setup(name='freeseer',
      version='1.9.6',
      description='video studio in a backpack',
      author='fosslc',
      author_email='fosslc@gmail.com',
      url='http://wiki.github.com/fosslc/freeseer/',
      license='GPLv3',
      data_files=[('/etc/modprobe.d', ['src/modprobe.d/vga2usb.conf']),
                  ('/etc/freeseer', ['src/config/logging.conf'])],
      packages=['freeseer'],
      package_dir={'freeseer': 'src'},
      package_data={'freeseer': ['freeseer', 'talks.txt']},
      )
