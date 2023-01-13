# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import sys

import requests
from six import text_type

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.parse import parse_qs, urlencode, urlparse


def fetch_url(prepared_request):  # type: ignore
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


class AWSV4SignerAuth(requests.auth.AuthBase):
    """
    AWS V4 Request Signer for Requests.
    """

    def __init__(self, credentials, region, service="es"):  # type: ignore
        if not credentials:
            raise ValueError("Credentials cannot be empty")
        self.credentials = credentials

        if not region:
            raise ValueError("Region cannot be empty")
        self.region = region

        if not service:
            raise ValueError("Service name cannot be empty")
        self.service = service

    def __call__(self, request):  # type: ignore
        return self._sign_request(request)  # type: ignore

    def _sign_request(self, prepared_request):  # type: ignore
        """
        This method helps in signing the request by injecting the required headers.
        :param prepared_request: unsigned request
        :return: signed request
        """

        import hashlib

        from botocore.auth import SigV4Auth
        from botocore.awsrequest import AWSRequest

        url = fetch_url(prepared_request)  # type: ignore

        # create an AWS request object and sign it using SigV4Auth
        aws_request = AWSRequest(
            method=prepared_request.method.upper(),
            url=url,
            data=prepared_request.body,
        )

        if hasattr(prepared_request, "body") and prepared_request.body is not None:
            if hasattr(prepared_request.body, "read"):
                prepared_request.body = prepared_request.body.read()
            self.encode_body(prepared_request)
            content_hash = hashlib.sha256(prepared_request.body)
        elif (
            hasattr(prepared_request, "content")
            and prepared_request.content is not None
        ):
            content_hash = hashlib.sha256(prepared_request.content)
        else:
            content_hash = hashlib.sha256(b"")

        prepared_request.headers["x-amz-content-sha256"] = content_hash.hexdigest()

        sig_v4_auth = SigV4Auth(self.credentials, self.service, self.region)
        sig_v4_auth.add_auth(aws_request)

        # copy the headers from AWS request object into the prepared_request
        prepared_request.headers.update(dict(aws_request.headers.items()))

        del prepared_request.headers["Content-Length"]

        return prepared_request

    # inspired by https://github.com/tedder/requests-aws4auth
    @staticmethod
    def encode_body(req):
        if isinstance(req.body, text_type):
            split = req.headers.get("content-type", "text/plain").split(";")
            if len(split) == 2:
                ct, cs = split
                cs = cs.split("=")[1]
                req.body = req.body.encode(cs)
            else:
                ct = split[0]
                if ct == "application/x-www-form-urlencoded" or "x-amz-" in ct:
                    req.body = req.body.encode()
                else:
                    req.body = req.body.encode("utf-8")
                    req.headers["content-type"] = ct + "; charset=utf-8"
