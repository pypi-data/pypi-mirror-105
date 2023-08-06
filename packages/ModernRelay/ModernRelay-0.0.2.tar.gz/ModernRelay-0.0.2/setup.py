# !/usr/bin/env python

from setuptools import setup

requirements = [
    'aiofiles',
    'aiohttp',
    'aiosmtpd',
    'APScheduler',
    'argon2-cffi',
    'confuse',
    'msgraph-async',
]

setup(
    name='modern-relay',
    packages=['ModernRelay', 'ModernRelay.tests'],
    version='0.0.2',
    description='An asynchronous SMTP relay with selectable delivery agents',
    author='Brett Buford',
    license='MIT',
    author_email='blbuford@gmail.com',
    url='https://github.com/blbuford/ModernRelay',
    keywords=['SMTP', 'Relay', ],
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require={
        'dev': [
            'asynctest',
            'check-manifest',
            'coverage',
            'flake8',
            'pytest',
            'pytest-asyncio',
            'pytest-cov',
            'pytest-sugar',
            'python-dotenv',
            'tox'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Communications :: Email',
    ],
)
