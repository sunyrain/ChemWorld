"""Tiny SDK for external Python programs; uses only the Python standard library."""

import json
import urllib.error
import urllib.request


class ChemLabClient:
    def __init__(self, base="http://127.0.0.1:8877", timeout=5):
        self.base = base.rstrip("/")
        self.timeout = timeout
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def request(self, path, data=None, method=None):
        q = urllib.request.Request(
            self.base + path,
            data=None if data is None else json.dumps(data).encode(),
            method=method or ("POST" if data is not None else "GET"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with self.opener.open(q, timeout=self.timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            raise ValueError(json.load(e).get("error", str(e))) from e

    def assets(self):
        return self.request("/api/v1/assets")["assets"]

    def get(self, id):
        return self.request(f"/api/v1/assets/{id}")

    def configure(self, id, **fields):
        return self.request(f"/api/v1/assets/{id}", fields, "PATCH")

    def action(self, id, action, **args):
        return self.request(f"/api/v1/assets/{id}/actions", dict(action=action, **args))

    def transfer(self, source_id, target_id, amount, unit="ml"):
        return self.request(
            "/api/v1/transfers",
            {"source_id": source_id, "target_id": target_id, "amount": amount, "unit": unit},
        )

    def result(self, id):
        return self.request("/api/v1/results/" + id)

    def csv(self, id):
        with self.opener.open(
            self.base + "/api/v1/results/" + id + ".csv", timeout=self.timeout
        ) as r:
            return r.read().decode("utf-8")
