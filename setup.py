import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pyang-arrcus-plugin',
    version='0.2',
    description=('A pyang plugin to validate Arrcus native models'),
    long_description=read('README.md'),
    packages=['plugins'],
    author='Mahesh Jethanandani',
    author_email='mjethanandani@gmail.com',
    license='New-style BSD',
    url='https://github.com/mjethanandani/pyang-arrcus-plugin',
    download_url='https://github.com/mjethanandani/pyang-arrcus-plugin/archive/0.2.tar.gz',
    install_requires=['pyang>=2.5.0'],
    include_package_data=True,
    keywords=['yang', 'validation'],
    classifiers=[],
    entry_points={'pyang.plugin': 'arrcus_pyang_plugin=plugins.arrcus:pyang_plugin_init'}
)
