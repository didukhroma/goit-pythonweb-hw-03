from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import urllib.parse
import mimetypes
import pathlib
import json


def write_data_to_file(data: dict) -> None:
    file_path = "./storage/data.json"
    logs = read_data_from_file()

    current_date = datetime.now().isoformat()
    logs[current_date] = data

    with open(file_path, "w") as file:
        json.dump(logs, file)


def read_data_from_file() -> dict:
    file_path = "./storage/data.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except:
        data = {}

    return data


def prepare_template():
    print("run function")
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("./template/template.jinja")
    logs = read_data_from_file()
    output = template.render(
        data=logs,
    )
    with open("read.html", "w") as f:
        f.write(output)


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        print(pr_url.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        elif pr_url.path == "/read":
            prepare_template()
            self.send_html_file("read.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        write_data_to_file(data_dict)
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()


def run(server_class=HTTPServer, handler_class=HttpHandler):
    # server_address = ("0.0.0.0", 3000)
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()
