from setuptools import find_packages, setup
setup(
    name='hvar',
    packages=find_packages(),
    version='0.1.0',
    description='HvarConsulting',
    author='HenriquePeixoto',
    license='MIT',
    install_requires=['xtarfile', 'pytest-shutil','google-cloud', 'datetime', 'google-api-client','google-oauth', 'google-oauth2-tool', 'requests', 'pybase64', 'pandas'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)