from setuptools import setup, find_packages
import os

try:
    import py2exe
except ImportError:
    pass

version = '0.1'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='HackSpark.SimpleDomotics',
      version=version,
      description="Simple Domotics from HackSpark",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Jonathan Schemoul',
      author_email='jonathan.schemoul@gmail.com',
      url='http://hackspark.fr/',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['HackSpark'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'bottle',
          'pyyaml',
          'paste',
          'cython'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """
      )
