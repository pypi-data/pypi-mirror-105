import os

from setuptools import find_namespace_packages, find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='mlservicewrapper-config',
   use_scm_version = True,
   description='Configuration helpers for ml services',
   author='Matthew Haugen',

   url="https://github.com/ml-service-wrapper/ml-service-wrapper-config",
   long_description=long_description,
   long_description_content_type="text/markdown",

   package_dir={"": "src"},
   packages=find_namespace_packages("src", include=['mlservicewrapper.*']),

   setup_requires=['setuptools_scm'],
   zip_safe=False,
   python_requires='>=3.6'
)
