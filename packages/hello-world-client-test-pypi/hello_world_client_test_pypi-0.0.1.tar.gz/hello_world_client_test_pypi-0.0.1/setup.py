#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
import datetime


def GetVersion():
    return '0.0.1'
    try:
        with open('./version', 'r') as f:
            version = f.read()
    except:
        now_time = datetime.datetime.now()
        version = "%s.%s.%s" % (
            now_time.strftime('%y') + now_time.strftime('%m'),
            now_time.strftime('%d') + now_time.strftime('%H'),
            now_time.strftime('%M') + now_time.strftime('%S'))
    return version


setup(name='hello_world_client_test_pypi',
      version=GetVersion(),
      author='hello world',
      include_package_data=True,
      zip_safe=False,
      url="https://pypi.org/",
      author_email='',
      python_requires=">=3.3",
      packages=['test_pypi_haha'],
      license="MIT",
      install_requires=[])
