from setuptools import find_packages, setup
from icetrust.utils import IcetrustUtils

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='icetrust',
    version=IcetrustUtils.get_version(),
    description='A tool for verification of software downloads using checksums and PGP.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nightwatchcybersecurity/icetrust',
    author='Nightwatch Cybersecurity',
    author_email='research@nightwatchcybersecurity.com',
    license='Apache',
    packages=find_packages(exclude=["scripts.*", "scripts", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'icetrust = icetrust.cli:cli'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    project_urls={
        'Bug Reports': 'https://github.com/nightwatchcybersecurity/icetrust/issues',
        'Source': 'https://github.com/nightwatchcybersecurity/icetrust',
    },
)
