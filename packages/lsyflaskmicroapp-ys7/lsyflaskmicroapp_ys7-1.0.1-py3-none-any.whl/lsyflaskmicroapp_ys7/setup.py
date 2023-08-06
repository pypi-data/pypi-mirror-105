# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='lsyflaskmicroapp-ys7',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests==2.24.0',
        'cacheout==0.11.1'
    ],
)
