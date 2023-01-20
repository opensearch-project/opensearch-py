# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import sys

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.parse import parse_qs, urlencode, urlparse


def sanitise_url(url, host):  # type: ignore
    """
    This is a util method that helps in reconstructing the request url.
    :param url
    :param query_string
    :param host
    :return: reconstructed url
    """
    url = urlparse(url)
    path = url.path or "/"

    querystring = ""
    if url.query:
        querystring = "?" + urlencode(
            parse_qs(url.query, keep_blank_values=True), doseq=True
        )

    location = host or url.netloc

    # construct the url and return
    return location + path + querystring


class AWSV4SignerAsyncAuth:
    """
    AWS V4 Request Signer for Async Requests.
    """

    def __init__(self, credentials, region, service="es"):  # type: ignore
        if not credentials:
            raise ValueError("Credentials cannot be empty")
        self.credentials = credentials

        if not region:
            raise ValueError("Region cannot be empty")
        self.region = region

    def __call__(self, method, url, body, host):  # type: ignore
        return self._sign_request(method, url, body, host)  # type: ignore
        
        if not service:
            raise ValueError("Service name cannot be empty")
        self.service = service

    def _sign_request(self, method, url, body, host):
        """
        This method helps in signing the request by injecting the required headers.
        :param prepared_request: unsigned headers
        :return: signed headers
        """

        from botocore.auth import SigV4Auth
        from botocore.awsrequest import AWSRequest

        url = sanitise_url(url, host)

        # create an AWS request object and sign it using SigV4Auth
        aws_request = AWSRequest(
            method=method,
            url=url,
        )

        sig_v4_auth = SigV4Auth(self.credentials, self.service, self.region)
        sig_v4_auth.add_auth(aws_request)

        # copy the headers from AWS request object into the prepared_request
        return dict(aws_request.headers.items())
