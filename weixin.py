from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class HttpServer(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/msg":
            json_str = self.rfile.read(int(self.headers["content-length"]))
            json_str = json_str.decode()
            result = json.loads(json_str)
            print(result)

            if result["msg_type"] == 1:
                print("收到文本消息：{}".format(result["data"]["content"]))

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"result": "ok"}).encode())


if __name__ == '__main__':
    host = ("127.0.0.1", 9008)
    server = HTTPServer(host, HttpServer)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()