from setuptools import find_packages, setup

setup(
    name='click-ui-unofficial',
    author='Rakesh Bute',
    version='0.0.1',
    license="Not Decided Yet. Likely to use python click framework license",
    packages=find_packages(),
    python_requires=">=3.*",
    install_requires=[
        'click'
    ]
)
