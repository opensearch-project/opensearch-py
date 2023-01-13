# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import sys

from six import text_type

PY3 = sys.version_info[0] == 3


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

        if not region:
            raise ValueError("Service name cannot be empty")
        self.service = service

    def __call__(self, method, url, query_string, body):  # type: ignore
        return self._sign_request(method, url, query_string, body)  # type: ignore

    def _sign_request(self, method, url, query_string, body):
        """
        This method helps in signing the request by injecting the required headers.
        :param prepared_request: unsigned headers
        :return: signed headers
        """
        import hashlib

        from botocore.auth import SigV4Auth
        from botocore.awsrequest import AWSRequest

        # create an AWS request object and sign it using SigV4Auth
        aws_request = AWSRequest(
            method=method,
            url="".join([url, query_string]),
            data=body,
        )

        if aws_request.body is not None:
            if hasattr(aws_request.body, "read"):
                aws_request.body = aws_request.body.read()
            self.encode_body(aws_request)
            content_hash = hashlib.sha256(aws_request.body)
        elif hasattr(aws_request, "content") and aws_request.content is not None:
            content_hash = hashlib.sha256(aws_request.content)
        else:
            content_hash = hashlib.sha256(b"")

        aws_request.headers["x-amz-content-sha256"] = content_hash.hexdigest()

        sig_v4_auth = SigV4Auth(self.credentials, self.service, self.region)
        sig_v4_auth.add_auth(aws_request)

        if "Content-Length" in aws_request.headers:
            del aws_request.headers["Content-Length"]

        # copy the headers from AWS request object into the prepared_request
        return dict(aws_request.headers.items())

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
