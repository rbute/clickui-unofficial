import os

from setuptools import find_packages, setup

description: str = ''

with open('README.MD', 'r') as r:
    description = r.read()
    del r

setup(
    name='clickui-unofficial',
    author='Rakesh Bute',
    description="Unofficial UI wrapper on click commands",
    long_description_content_type='text/markdown',
    long_description=description,
    author_email=os.getenv('MY_EMAIL', ''),
    version='0.5.0',
    license="BSD-3-Clause",
    packages=find_packages(),
    python_requires=">=3.*",
    project_urls={
        "Code": "https://github.com/rbute/clickui-unofficial",
    },
    install_requires=[
        'click',
        'tkcalendar',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ]
)
