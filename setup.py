from setuptools import setup, find_packages

setup(
    name='colab-sync',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
    ],
    entry_points={
        'console_scripts': [
            'colab=cli.main:main',
        ],
    },
)
