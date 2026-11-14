import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HTML = Path(__file__).with_name("index.html").read_bytes()

def parse(expression):
    def visit(i):
        if i >= len(expression):
            raise ValueError("不完整的 SK 表達式")
        c = expression[i]
        if c in ("S", "K"):
            return c, i + 1
        if c != "@":
            raise ValueError("僅允許 @、S、K")
        left, j = visit(i + 1)
        right, k = visit(j)
        return (left, right), k
    tree, end = visit(0)
    if end != len(expression):
        raise ValueError("多餘的符號")
    return tree

def encode(tree):
    if isinstance(tree, str):
        return tree
    return "@" + encode(tree[0]) + encode(tree[1])

def reduce_once(tree):
    if isinstance(tree, str):
        return None
    args = []
    head = tree
    while isinstance(head, tuple):
        args.insert(0, head[1])
        head = head[0]
    if head == "K" and len(args) >= 2:
        replacement, rest = args[0], args[2:]
    elif head == "S" and len(args) >= 3:
        replacement = ((args[0], args[2]), (args[1], args[2]))
        rest = args[3:]
    else:
        left = reduce_once(tree[0])
        if left is not None:
            return (left, tree[1])
        right = reduce_once(tree[1])
        return (tree[0], right) if right is not None else None
    for value in rest:
        replacement = (replacement, value)
    return replacement

def calculate(expression, budget=30):
    if not isinstance(expression, str) or not 0 < len(expression) <= 300:
        raise ValueError("表達式長度必須介於 1 到 300 字元")
    if not isinstance(budget, int) or not 0 <= budget <= 100:
        raise ValueError("預算必須介於 0 到 100")
    tree = parse(expression)
    trace = [expression]
    for _ in range(budget):
        updated = reduce_once(tree)
        if updated is None:
            break
        tree = updated
        output = encode(tree)
        if len(output) > 10000:
            return {"trace": trace, "result": trace[-1], "steps": len(trace) - 1, "status": "UNRESOLVED", "reason": "OUTPUT_LIMIT"}
        trace.append(output)
    return {
        "trace": trace,
        "result": trace[-1],
        "steps": len(trace) - 1,
        "status": "NORMAL" if reduce_once(tree) is None else "UNRESOLVED",
    }

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/health"):
            self.send_error(404)
            return
        if self.path == "/health":
            self.respond(200, {"status": "ok"})
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(HTML)))
        self.end_headers()
        self.wfile.write(HTML)

    def respond(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/sk":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 4096:
                raise ValueError("請提供小於 4096 位元組的 JSON")
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict):
                raise ValueError("請提供 JSON 物件")
            result = calculate(payload["expression"], payload.get("budget", 30))
            self.respond(200, result)
        except (ValueError, KeyError, TypeError, RecursionError) as error:
            self.respond(400, {"error": str(error)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
