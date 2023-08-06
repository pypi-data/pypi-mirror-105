from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='dkcalculator',
    version='1.0.0',
    description='A very basic calculator functionality implemented with Python 3',
    license="MIT",
    long_description=long_description,
    author='Dovile Kuznecova',
    author_email='dovileobo@gmail.com',
    packages=['calculator'],
    install_requires=['typing'],
    tests_require=['pytest']
)
