"""Local REST service. No third-party Python dependencies."""

import argparse
import csv
import io
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .catalog import API_PORT, ASSETS, VERSION
from .engine import Lab, LabError, exact_keys

ROOT = Path(__file__).resolve().parent


def openapi():
    error = {
        "description": "Validation error or device conflict",
        "content": {
            "application/json": {
                "schema": {"type": "object", "properties": {"error": {"type": "string"}}}
            }
        },
    }

    def operation(summary, schema=None):
        op = {
            "summary": summary,
            "responses": {
                "200": {"description": "Success; response includes state, revision, or result"},
                "404": error,
                "409": error,
                "422": error,
            },
        }
        if schema is not None:
            op["requestBody"] = {
                "required": True,
                "content": {"application/json": {"schema": schema}},
            }
        return op

    def obj(props, required=None):
        return {
            "type": "object",
            "properties": props,
            "additionalProperties": False,
            "required": list(props) if required is None else required,
        }

    string = {"type": "string"}
    transfer = obj(
        {
            "source_id": string,
            "target_id": string,
            "amount": {"type": "number", "exclusiveMinimum": 0},
            "unit": {"enum": ["ml", "g"]},
        }
    )
    paths = {
        "/health": {"get": operation("Service and live Blender bridge health")},
        "/api/v1/assets": {"get": operation("List every individually addressable asset")},
        "/api/v1/state": {"get": operation("Atomic state snapshot for scene synchronization")},
        "/api/v1/transfers": {
            "post": operation("Atomic inventory transfer between containers", transfer)
        },
        "/api/v1/results": {"get": operation("List measurement result summaries")},
        "/api/v1/results/{result_id}": {
            "parameters": [{"in": "path", "name": "result_id", "required": True, "schema": string}],
            "get": operation("Result JSON, or append .csv for numeric export"),
        },
        "/api/v1/events": {
            "get": operation("Latest 500 recorded commands; optional ?after=revision")
        },
    }
    from .environment_api import extend_openapi

    extend_openapi(paths, operation)
    for a in ASSETS:
        path = "/api/v1/assets/" + a["id"]
        paths[path] = {"get": operation(a["name"] + " — metadata, state, capabilities, and pose")}
        if a["fields"]:
            props = {
                k: {kk: vv for kk, vv in v.items() if kk != "unit"}
                | {"description": v.get("unit", "")}
                for k, v in a["fields"].items()
            }
            schema = obj(props, [])
            schema["minProperties"] = 1
            paths[path]["patch"] = operation("Configure " + a["id"], schema)
        variants = []
        for action in a["actions"]:
            fields = {"action": {"const": action}}
            if action in {"measure", "weigh"}:
                fields["sample_id"] = string
            if action == "dispense":
                fields.update(
                    target_id=string,
                    amount={"type": "number", "exclusiveMinimum": 0},
                    unit={"enum": [a["unit"]]},
                )
            if action == "set_visible":
                fields["visible"] = {"type": "boolean"}
            if action == "move":
                fields["position_m"] = {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 3,
                    "maxItems": 3,
                }
            if action == "navigate":
                fields["station"] = {"enum": ["home", "preparation", "analysis", "reaction"]}
            if action == "pick":
                fields["asset_id"] = string
            if action == "place":
                fields["station"] = {"enum": ["preparation", "analysis"]}
            variants.append(obj(fields))
        paths[path + "/actions"] = {"post": operation("Operate " + a["id"], {"oneOf": variants})}
    from .projection import FRAME_KEYS

    frame = obj({key: {} for key in sorted(FRAME_KEYS)})
    frame["properties"]["schema_version"] = {"const": "chemworld-blender-public-1"}
    frame["properties"]["physical_control_enabled"] = {"const": False}
    paths["/api/v1/chemworld/frame"] = {
        "get": operation("Read the last public ChemWorld presentation frame"),
        "post": operation(
            "Publish an ordered public frame without changing scene inventory", frame
        ),
    }
    paths["/api/v1/chemworld/release"] = {
        "post": operation(
            "Release scene ownership; preserve the last public frame", obj({"session_id": string})
        ),
    }
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "ChemLab Virtual Laboratory",
            "version": VERSION,
            "description": (
                "Virtual devices only. Scene simulation and "
                "public ChemWorld observations have separate provenance."
            ),
        },
        "servers": [{"url": "/"}],
        "paths": paths,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "ChemLab/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        if "/bridge" not in str(args) and "/state" not in str(args):
            print(time.strftime("%H:%M:%S"), fmt % args, flush=True)

    def respond(self, payload, status=200, content_type="application/json; charset=utf-8"):
        body = (
            json.dumps(payload, ensure_ascii=False, allow_nan=False)
            if content_type.startswith("application/json")
            else payload
        ).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def body(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 65536:
                raise LabError("JSON body required; maximum 64 KiB", 413)
            return json.loads(
                self.rfile.read(length),
                parse_constant=lambda v: (_ for _ in ()).throw(ValueError("Non-finite number")),
            )
        except (ValueError, UnicodeError) as e:
            raise LabError("Invalid JSON body") from e

    def dispatch(self, method):
        lab = self.server.lab
        url = urlsplit(self.path)
        path = url.path.rstrip("/") or "/"
        try:
            if path == "/api/v1/chemworld/frame":
                self.respond(
                    lab.projection.snapshot()
                    if method == "GET"
                    else lab.projection.publish(self.body())
                    if method == "POST"
                    else {"error": "Unsupported method"},
                    200 if method in {"GET", "POST"} else 405,
                )
                return
            if path == "/api/v1/chemworld/release" and method == "POST":
                self.respond(lab.projection.release(self.body()))
                return
            if path == "/api/v1/environment" or path.startswith("/api/v1/environment/"):
                from .environment_api import dispatch_environment

                self.respond(
                    dispatch_environment(
                        lab.environment,
                        method,
                        path,
                        self.body if method in {"POST", "PATCH"} else None,
                    )
                )
                return
            if method == "GET":
                if path in {"/", "/docs"}:
                    rows = "\n".join(
                        f"{a['id']:<22} {a['kind']:<12} {a['name']}\n"
                        f"  GET/PATCH /api/v1/assets/{a['id']}\n"
                        f"  POST /api/v1/assets/{a['id']}/actions\n"
                        for a in ASSETS
                    )
                    self.respond(
                        "ChemWorld Blender Lab\n\nOpenAPI 3.1: /openapi.json\n"
                        "Core observations, scene simulation and external observations "
                        "are separate.\n\n" + rows,
                        content_type="text/plain; charset=utf-8",
                    )
                    return
                if path == "/openapi.json":
                    result = openapi()
                elif path == "/health":
                    result = lab.health()
                elif path == "/api/v1/assets":
                    result = {"assets": [lab.get(a["id"]) for a in ASSETS], "count": len(ASSETS)}
                elif path == "/api/v1/state":
                    result = lab.snapshot()
                elif path == "/api/v1/events":
                    try:
                        after = int(parse_qs(url.query).get("after", ["-1"])[0])
                    except ValueError:
                        raise LabError("after must be an integer") from None
                    with lab.lock:
                        result = {"events": [e.copy() for e in lab.events if e["revision"] > after]}
                elif path == "/api/v1/results":
                    with lab.lock:
                        result = {
                            "results": [
                                {
                                    k: v
                                    for k, v in r.items()
                                    if k not in {"sample_snapshot", "x", "y"}
                                }
                                for r in lab.results.values()
                            ]
                        }
                elif path.startswith("/api/v1/results/"):
                    rid = path.split("/")[-1]
                    as_csv = rid.endswith(".csv")
                    if as_csv:
                        rid = rid[:-4]
                    with lab.lock:
                        result = lab.results.get(rid)
                    if result is None:
                        raise LabError("Result not found", 404)
                    if as_csv:
                        output = io.StringIO(newline="")
                        writer = csv.writer(output)
                        writer.writerow(["mode", result["mode"]])
                        if result["kind"] == "spectrum":
                            writer.writerow([result["x_unit"], result["y_unit"]])
                            writer.writerows(zip(result["x"], result["y"], strict=False))
                        else:
                            writer.writerow(["value", "unit"])
                            writer.writerow(
                                [
                                    result.get("value", result.get("volume_ml", "")),
                                    result.get("unit", "ml"),
                                ]
                            )
                        self.respond(output.getvalue(), content_type="text/csv; charset=utf-8")
                        return
                elif path.startswith("/api/v1/assets/") and len(path.split("/")) == 5:
                    result = lab.get(path.split("/")[-1])
                else:
                    raise LabError("Endpoint not found", 404)
            elif (
                method == "PATCH"
                and path.startswith("/api/v1/assets/")
                and len(path.split("/")) == 5
            ):
                result = lab.patch(path.split("/")[-1], self.body())
            elif method == "POST":
                if path == "/api/v1/transfers":
                    result = lab.transfer(self.body())
                elif path == "/api/v1/bridge":
                    data = self.body()
                    exact_keys(data, ["applied_revision", "object_count", "file", "errors"])
                    if (
                        type(data.get("applied_revision")) is not int
                        or type(data.get("object_count")) is not int
                        or not isinstance(data.get("errors"), list)
                    ):
                        raise LabError("Invalid bridge acknowledgement")
                    with lab.lock:
                        lab.bridge = data
                        lab.last_bridge = time.time()
                    result = {"ok": True}
                elif (
                    path.startswith("/api/v1/assets/")
                    and path.endswith("/actions")
                    and len(path.split("/")) == 6
                ):
                    result = lab.action(path.split("/")[-2], self.body())
                else:
                    raise LabError("Endpoint not found", 404)
            else:
                raise LabError("Endpoint/method not found", 404)
            self.respond(result)
        except LabError as e:
            self.respond({"error": str(e)}, e.status)
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception:
            import traceback

            traceback.print_exc()
            self.respond({"error": "Internal server error; see service log"}, 500)

    def do_GET(self):
        self.dispatch("GET")

    def do_PATCH(self):
        self.dispatch("PATCH")

    def do_POST(self):
        self.dispatch("POST")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=API_PORT)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "runtime")
    args = parser.parse_args()
    lab = Lab(args.data_dir)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.daemon_threads = True
    server.lab = lab
    stop = threading.Event()

    def ticker():
        while not stop.wait(0.5):
            lab.tick()

    threading.Thread(target=ticker, daemon=True).start()
    print(f"ChemLab ready: http://127.0.0.1:{args.port} / {len(ASSETS)} assets", flush=True)
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        server.server_close()
        with lab.lock:
            lab.save()


if __name__ == "__main__":
    main()
