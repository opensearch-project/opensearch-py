# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import re
from os.path import abspath, dirname, join

from setuptools import find_packages, setup

PACKAGE_NAME = "opensearch-py"
PACKAGE_VERSION = ""
BASE_DIR = abspath(dirname(__file__))

with open(
    join(BASE_DIR, PACKAGE_NAME.replace("-", ""), "_version.py"), encoding="utf-8"
) as f:
    data = f.read()
    m = re.search(r"^__versionstr__: str\s+=\s+[\"\']([^\"\']+)[\"\']", data, re.M)
    if m:
        PACKAGE_VERSION = m.group(1)
    else:
        raise Exception(f"Invalid version: {data}")

with open(join(BASE_DIR, "README.md"), encoding="utf-8") as f:
    long_description = f.read().strip()

MODULE_DIR = PACKAGE_NAME.replace("-", "")
packages = [
    package
    for package in find_packages(where=".", exclude=("test_opensearchpy*",))
    if package == MODULE_DIR or package.startswith(MODULE_DIR + ".")
]
install_requires = [
    'urllib3>=1.26.19,<1.27 ; python_version < "3.10"',
    'urllib3>=1.26.19,!=2.2.0,!=2.2.1,<3 ; python_version >= "3.10"',
    "requests>=2.32.0, <3.0.0",
    "python-dateutil",
    "certifi>=2024.07.04",
    "Events",
]
tests_require = [
    "requests>=2.0.0, <3.0.0",
    "coverage<8.0.0",
    "pyyaml",
    "pytest>=3.0.0",
    "pytest-cov",
    "pytz",
    "botocore",
    "pytest-mock<4.0.0",
]

async_require = ["aiohttp>=3.12.14,<4"]

docs_require = ["sphinx", "sphinx_rtd_theme", "myst_parser", "sphinx_copybutton"]
generate_require = ["black>=24.3.0", "jinja2"]

setup(
    name=PACKAGE_NAME,
    description="Python client for OpenSearch",
    license="Apache-2.0",
    url="https://github.com/opensearch-project/opensearch-py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=PACKAGE_VERSION,
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
    package_data={"opensearchpy": ["py.typed"]},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=3.8, <4",
    install_requires=install_requires,
    test_suite="test_opensearchpy.run_tests.run_all",
    tests_require=tests_require,
    extras_require={
        "develop": tests_require + docs_require + generate_require,
        "docs": docs_require + async_require,
        "async": async_require,
        "kerberos": ["requests_kerberos"],
    },
)
