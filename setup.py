#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-produtos-crawler",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_produtos_crawler"],
    install_requires=[
        "singer-python==5.12.2",
        "requests==2.27.1",
        "lxml==4.7.1",
        "pandas==1.1.5",
        "selenium==4.0.0a7",
        "beautifulsoup4==4.10.0",
        "XlsxWriter==3.0.2",
        "webdriver-manager==3.5.3",
        "google-cloud-storage==2.1.0",
        "six",
        "charset_normalizer"
    ],
    entry_points="""
    [console_scripts]
    tap-produtos-crawler=tap_produtos_crawler:main
    """,
    packages=["tap_produtos_crawler"],
    package_data={"schemas": ["tap_produtos_crawler/schemas/*.json"]},
    include_package_data=True,
)
