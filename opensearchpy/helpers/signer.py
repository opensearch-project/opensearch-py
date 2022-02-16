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

import sys

import requests

from ..exceptions import ImproperlyConfigured

OPENSEARCH_SERVICE = "es"


def python_version_gte_36():  # type: ignore
    """
    A util method to check python version.
    :return: boolean that returns true if python version running is greater than
    equal to 3.6 otherwise returns false
    """
    if sys.hexversion >= 0x03060000:
        return True
    else:
        return False


try:
    if python_version_gte_36():  # type: ignore
        from urllib.parse import parse_qs, urlencode, urlparse
except ImportError:
    raise ImproperlyConfigured(
        "Please upgrade the python version to 3.6 or above to use AWS Signer."
    )


class AWSV4Signer(requests.auth.AuthBase):
    """
    AWS V4 Request Signer for Requests.
    """

    def __init__(self, credentials, region):  # type: ignore
        if not region:
            raise ValueError("AWS region can not be null")
        self.credentials = credentials
        self.region = region

    def __call__(self, request):  # type: ignore
        if python_version_gte_36():  # type: ignore
            return self.inject_headers(request)  # type: ignore
        else:
            raise ImproperlyConfigured(
                "Please upgrade the python version to 3.6 or above to use AWS Signer."
            )

    def inject_headers(self, prepared_request):  # type: ignore
        """
        This method helps in signing the request by injecting the required headers.
        :param prepared_request: unsigned request
        :return: signed request
        """
        try:
            from botocore.auth import SigV4Auth
            from botocore.awsrequest import AWSRequest

            url = self.fetch_url(prepared_request)  # type: ignore

            # create an AWS request object and sign it using SigV4Auth
            aws_request = AWSRequest(
                method=prepared_request.method.upper(),
                url=url,
                data=prepared_request.body,
            )
            SigV4Auth(self.credentials, OPENSEARCH_SERVICE, self.region).add_auth(
                aws_request
            )

            # copy the headers from AWS request object into the prepared_request
            prepared_request.headers.update(dict(aws_request.headers.items()))

            return prepared_request
        except ImportError:
            raise ImproperlyConfigured("Please install botocore to use AwsV4Signer.")

    def fetch_url(self, prepared_request):  # type: ignore
        """
        This is a util method that helps in reconstructing the request url.
        :param prepared_request: unsigned request
        :return: reconstructed url
        """
        url = urlparse(prepared_request.url)
        path = url.path or "/"

        # fetch the query string if present in the request
        querystring = ""
        if url.query:
            querystring = "?" + urlencode(
                parse_qs(url.query, keep_blank_values=True), doseq=True
            )

        # fetch the host information from headers
        headers = dict(
            (key.lower(), value) for key, value in prepared_request.headers.items()
        )
        location = headers.get("host") or url.netloc

        # construct the url and return
        return url.scheme + "://" + location + path + querystring
