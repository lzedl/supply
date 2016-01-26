# -*- coding: utf8 -*-
from distutils.core import setup


setup(
    name='zsupply',
    version='0.1',
    author='Alexandr Litovchenko',
    author_email='zedlaa@gmail.com',
    scripts=['z-autoset-screen.py'],
    requires=['PyYAML'],
    data_files=[('/etc', ['config/zsupply.yml']),
                ('/etc/udev/rules.d', ['config/50-z-udev.rules']),
                ('/usr/share/zsupply', ['config/zsupply.yml'])],
    url='unknown',
    description=''
)
