import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-geode-geocoding',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A simple Django app to request geocoding information',
    long_description=README,
    url='https://www.opengeode.be/',
    author='Raphael Sprumont',
    author_email='raphael.sprumont@opengeode.be',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Geocoding',
    ],
)
