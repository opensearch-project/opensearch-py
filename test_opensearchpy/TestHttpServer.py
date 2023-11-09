# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any


class TestHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        headers = self.headers

        if self.path == "/redirect":
            new_location = "http://localhost:8090"
            self.send_response(302)
            self.send_header("Location", new_location)
        else:
            self.send_response(200)
            self.send_header("Content-type", "application/json")

        self.end_headers()

        Headers = {}
        for header, value in headers.items():
            capitalized_header = "-".join([word.title() for word in header.split("-")])
            Headers.update({capitalized_header: value})
        if "Connection" in Headers:
            Headers.pop("Connection")

        data = {"method": "GET", "headers": Headers}
        self.wfile.write(json.dumps(data).encode("utf-8"))


class TestHTTPServer(HTTPServer):
    __test__ = False
    _server_thread: Any

    def __init__(self, host: str = "localhost", port: int = 8080) -> None:
        super().__init__((host, port), TestHTTPRequestHandler)
        self._server_thread = None

    def start(self) -> None:
        if self._server_thread is not None:
            return

        self._server_thread = threading.Thread(target=self.serve_forever)
        self._server_thread.start()

    def stop(self) -> None:
        if self._server_thread is None:
            return
        self.socket.close()
        self.shutdown()
        self._server_thread.join()
        self._server_thread = None
