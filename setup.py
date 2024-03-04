from setuptools import setup, find_packages

setup(
    name='CacheKing',
    version='0.1.0',
    author='Waleed Alasad',
    description='An analytical tool for optimizing and analyzing Python application performance through caching.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Wa-lead/cacheking',
    packages=find_packages(),
    install_requires=[
        'prettytable',  # For generating the caching report tables
    ],

)
