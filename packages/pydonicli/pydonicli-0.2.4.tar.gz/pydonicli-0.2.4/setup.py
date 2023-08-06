from setuptools import setup, find_packages

setup(
    name='pydonicli',
    version=open('version').read(),
    description='pydoni-cli is a Python library that serves as a command-line interface to custom-built tools developed by Andoni Sooklaris.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    long_description_content_type='text/markdown',
    author='Andoni Sooklaris',
    author_email='andoni.sooklaris@gmail.com',
    url='https://github.com/tsouchlarakis/pydoni-cli',
    license=open('LICENSE').read(),
    install_requires=open('requirements.in').read(),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points=open('entry_points.ini').read(),
    include_package_data=True,
    test_suite='tests'
)
