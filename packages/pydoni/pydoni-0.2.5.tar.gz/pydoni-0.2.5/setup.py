from setuptools import setup

setup(
    name='pydoni',
    version=open('version').read(),
    description='A Python module for custom-built tools and maintained by Andoni Sooklaris.',
    # long_description_content_type='text/markdown',
    # long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    author='Andoni Sooklaris',
    author_email='andoni.sooklaris@gmail.com',
    url='https://github.com/tsouchlarakis/pydoni',
    license=open('LICENSE').read(),
    install_requires=open('requirements.in').read(),
    # package_dir={'': 'pydoni'},
    packages=['pydoni'],  # Directory name in same directory as setup.py
    include_package_data=True,
    test_suite='tests'
)
