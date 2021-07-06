from setuptools import setup, find_packages

setup(
    name='project-sat3',
    version='0.1.0.dev0',
    packages=find_packages(),
    description='Solution to project Euler problems',
    install_requires=[line for line in open('requirements.txt')],
    include_package_data=True,
)
