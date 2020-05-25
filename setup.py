from setuptools import find_packages, setup

setup(
    name='click-ui-unofficial',
    author='Rakesh Bute',
    version='0.2.0',
    license="BSD-3-Clause",
    packages=find_packages(),
    python_requires=">=3.*",
    install_requires=[
        'click'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ]
)
