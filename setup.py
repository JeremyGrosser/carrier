from setuptools import setup

setup(  name='Carrier',
        version='0.1',
        description='A RESTful KVM control daemon',
        author='Jeremy Grosser',
        author_email='code@synack.me',
        url='http://synack.github.com/carrier/',
        packages=['carrier'],
        scripts=['scripts/carrierd'],
        install_requires=['bottle'],
    )
