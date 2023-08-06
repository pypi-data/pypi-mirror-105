"""Setup Module for Datalayer Admin.
"""
import setuptools

VERSION = '0.0.3'

setuptools.setup(
    name = 'clouder',
    version = VERSION,
    description = 'Clouder',
    long_description = open('README.md').read(),
    packages = setuptools.find_packages(),
    package_dsp = {
        'clouder': [
            '*',
        ],
    },
    install_requires = [
        'boto3',
        'configparser',
        'docker',
        'kubernetes',
        'pandas',
        'pathlib',
        'requests',
        'urllib3',
    ],
    extras_require = {
        'test': [
            'pytest',
            'pytest-cov',
            'pylint',
        ]
    },
    entry_points={
        'console_scripts': [
            'clouder=clouder.__main__:main',
        ]
    }
)
