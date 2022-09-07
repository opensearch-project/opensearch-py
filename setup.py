# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import re
from os.path import abspath, dirname, join

from setuptools import find_packages, setup

package_name = "opensearch-py"
base_dir = abspath(dirname(__file__))

with open(join(base_dir, package_name.replace("-", ""), "_version.py")) as f:
    package_version = re.search(
        r"__versionstr__\s+=\s+[\"\']([^\"\']+)[\"\']", f.read()
    ).group(1)

with open(join(base_dir, "README.md")) as f:
    long_description = f.read().strip()

module_dir = package_name.replace("-", "")
packages = [
    package
    for package in find_packages(where=".", exclude=("test_opensearchpy*",))
    if package == module_dir or package.startswith(module_dir + ".")
]

install_requires = [
    "urllib3>=1.21.1, <2",
    "certifi",
    "requests>=2.4.0, <3.0.0",
]
tests_require = [
    "requests>=2.0.0, <3.0.0",
    "coverage",
    "mock",
    "pyyaml",
    "pytest",
    "pytest-cov",
    "botocore;python_version>='3.6'",
]
async_require = ["aiohttp>=3,<4"]

docs_require = ["sphinx", "sphinx_rtd_theme", "myst_parser", "sphinx_copybutton"]
generate_require = ["black", "jinja2"]

setup(
    name=package_name,
    description="Python low-level client for OpenSearch",
    license="Apache-2.0",
    url="https://github.com/opensearch-project/opensearch-py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=package_version,
    author="Aleksei Atavin, Denis Zalevskiy, Rushi Agrawal, Shephali Mittal",
    author_email="axeo@aiven.io, dez@aiven.io, rushi.agr@gmail.com, shephalm@amazon.com",
    maintainer="Aleksei Atavin, Denis Zalevskiy, Rushi Agrawal, Shephali Mittal",
    maintainer_email="axeo@aiven.io, dez@aiven.io, rushi.agr@gmail.com, shephalm@amazon.com",
    project_urls={
        "Documentation": "https://opensearch.org/docs/clients/python",
        "Source Code": "https://github.com/opensearch-project/opensearch-py",
        "Issue Tracker": "https://github.com/opensearch-project/opensearch-py/issues",
    },
    packages=packages,
    package_data={"opensearchpy": ["py.typed", "*.pyi"]},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
    install_requires=install_requires,
    test_suite="test_opensearchpy.run_tests.run_all",
    tests_require=tests_require,
    extras_require={
        "develop": tests_require + docs_require + generate_require,
        "docs": docs_require,
        "async": async_require,
    },
)
