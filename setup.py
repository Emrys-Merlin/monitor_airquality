from importlib.metadata import entry_points

from setuptools import find_packages, setup

setup(
    name='monitor_airquality',
    version='0.1',
    url='',
    author='Tim Adler',
    author_email='tim+github@emrys-merlin.de',
    description='Measure airquality using some sensors connected to a raspberry pi',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': ['monitor_airquality=monitor_airquality.main:main']
    }
)
