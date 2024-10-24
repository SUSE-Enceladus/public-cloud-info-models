#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Setup script."""

from setuptools import find_packages, setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()

with open('requirements-test.txt') as req_file:
    test_requirements = req_file.read().splitlines()[2:]

with open('requirements-dev.txt') as req_file:
    dev_requirements = test_requirements + req_file.read().splitlines()[2:]


setup(
    name='pint-models',
    version='0.0.1',
    description='Contains a set of models and utilites for SUSE Pint Server.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='SUSE',
    author_email='public-cloud-dev@susecloud.net',
    url='https://github.com/SUSE-Enceladus/public-cloud-info-models',
    packages=find_packages(),
    package_dir={
        'pint_models': 'pint_models'
    },
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
        'test': test_requirements
    },
    license='GPLv3+',
    zip_safe=False,
    keywords='pint_models pint-models',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)','Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
)
