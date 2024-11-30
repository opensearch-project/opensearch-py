# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, Dict, Optional, Union
from urllib.parse import parse_qs, urlencode, urlparse


class AWSV4SignerAsyncAuth:
    """
    AWS V4 Request Signer for Async Requests.
    """

    def __init__(self, credentials: Any, region: str, service: str = "es") -> None:
        if not credentials:
            raise ValueError("Credentials cannot be empty")
        self.credentials = credentials

        if not region:
            raise ValueError("Region cannot be empty")
        self.region = region

        if not service:
            raise ValueError("Service name cannot be empty")
        self.service = service

    def __call__(
        self,
        method: str,
        url: str,
        query_string: Optional[str] = None,
        body: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        return self._sign_request(method, url, query_string, body, headers)

    def _sign_request(
        self,
        method: str,
        url: str,
        query_string: Optional[str],
        body: Optional[Union[str, bytes]],
        headers: Optional[Dict[str, str]],
    ) -> Dict[str, str]:
        """
        This method helps in signing the request by injecting the required headers.
        :param prepared_request: unsigned headers
        :return: signed headers
        """

        from botocore.auth import SigV4Auth
        from botocore.awsrequest import AWSRequest

        signature_host = self._fetch_url(url, headers or dict())

        # create an AWS request object and sign it using SigV4Auth
        aws_request = AWSRequest(
            method=method,
            url=signature_host,
            data=body,
        )

        # credentials objects expose access_key, secret_key and token attributes
        # via @property annotations that call _refresh() on every access,
        # creating a race condition if the credentials expire before secret_key
        # is called but after access_key- the end result is the access_key doesn't
        # correspond to the secret_key used to sign the request. To avoid this,
        # get_frozen_credentials() which returns non-refreshing credentials is
        # called if it exists.
        credentials = (
            self.credentials.get_frozen_credentials()
            if hasattr(self.credentials, "get_frozen_credentials")
            and callable(self.credentials.get_frozen_credentials)
            else self.credentials
        )

        sig_v4_auth = SigV4Auth(credentials, self.service, self.region)
        sig_v4_auth.add_auth(aws_request)
        aws_request.headers["X-Amz-Content-SHA256"] = sig_v4_auth.payload(aws_request)

        # copy the headers from AWS request object into the prepared_request
        return dict(aws_request.headers.items())

    def _fetch_url(self, url: str, headers: Optional[Dict[str, str]]) -> str:
        """
        This is a util method that helps in reconstructing the request url.
        :param prepared_request: unsigned request
        :return: reconstructed url
        """
        parsed_url = urlparse(url)
        path = parsed_url.path or "/"

        # fetch the query string if present in the request
        querystring = ""
        if parsed_url.query:
            querystring = "?" + urlencode(
                parse_qs(parsed_url.query, keep_blank_values=True), doseq=True
            )

        # fetch the host information from headers
        headers = {key.lower(): value for key, value in (headers or dict()).items()}
        location = headers.get("host") or parsed_url.netloc

        # construct the url and return
        return parsed_url.scheme + "://" + location + path + querystring
