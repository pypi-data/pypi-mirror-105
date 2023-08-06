# to run: python setup.py install
import numpy as np

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import setup
#from distutils.extension import Extension

setup(name="astromet",
      version='1.0.4',
      description='One and two body astrometry',
      author='Zephyr Penoyre',
      author_email='zephyrpenoyre@gmail.com',
      url='https://github.com/zpenoyre/astromet.py',
      license='GNU GPLv3',
      include_dirs=[np.get_include()],
      install_requires=['numpy','astropy','scipy'],
      )
