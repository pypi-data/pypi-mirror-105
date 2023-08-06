from setuptools import setup, find_packages
import sys, os

version = '0.0.2'

setup(name='dataapi5',
      version=version,
      description="test",
      long_description="""\
test""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Fzblww926',
      author='zbfang',
      author_email='13174444400@163.com',
      url='https://www.baidu.com',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
