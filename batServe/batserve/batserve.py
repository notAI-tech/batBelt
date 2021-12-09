import rich


def get_args():
    import argparse

    class ArgumentParser(argparse.ArgumentParser):
        def _print_message(self, message, file=None):
            rich.print(message)

    parser = ArgumentParser(
        description="[green]batBelt[/green] file server (1.0-rc5) - simple and useful file server"
    )
    parser.add_argument(
        "--host",
        help="Serve on host (eg: localhost, 0.0.0.0). Defaults to 0.0.0.0",
        nargs="?",
    )
    parser.add_argument("--port", help="Serve on port. Defaults to 8080", nargs="?")
    parser.add_argument(
        "--public",
        dest="public",
        action="store_true",
        help="Serve on a [yellow]publicly accessible URL[/yellow]",
    )
    parser.add_argument(
        "--no-index",
        dest="index",
        action="store_false",
        help="Disable auto-generation of index.html",
    )
    parser.add_argument(
        "--no-symlinks",
        dest="symlinks",
        action="store_false",
        help="Don't follow symlinks",
    )
    parser.add_argument(
        "--dir", help="The directory path to serve. Defaults to ./", nargs="?"
    )
    parser.add_argument(
        "-u",
        "--username",
        help="[yellow]Username[/yellow] for security, not set by default",
        nargs="?",
    )
    parser.add_argument(
        "-p",
        "--password",
        help="[yellow]Password[/yellow] for security, not set by default",
        nargs="?",
    )

    args, _ = parser.parse_known_args()

    return args


args = get_args()

from gevent import monkey

monkey.patch_all()

import os
import sys
import glob
import time
import uuid
import time
import atexit
import falcon
import signal
import gevent
import shutil
import psutil
import socket
import logging
import tempfile
import datetime
import mimetypes
import gunicorn.app.base
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO, format="%(message)s", handlers=[RichHandler(markup=True)]
)


class fileServer(object):
    def __init__(self, dir, no_index, no_symlinks):
        self.dir = dir
        self.no_index = no_index
        self.no_symlinks = no_symlinks

    def on_get(self, req, resp):
        try:
            logging.info(f"{req.remote_addr}, {req.relative_uri}")
            in_path = os.path.join(self.dir, req.relative_uri.strip().lstrip("/"))

            if os.path.isdir(in_path):
                if os.path.exists(os.path.join(in_path, "index.html")):
                    resp.content_type = "text/html"
                    resp.stream = open(os.path.join(in_path, "index.html"), "rb")
                elif self.no_index:
                    resp.media = (
                        "index.html doesn't exist and auto-generation is disabled"
                    )
                    resp.status = falcon.HTTP_404
                else:
                    html_rows = [
                        f"<tr> <td> <b> File </b> </td> <td> <b> Size (MB) </b> </td> <td> <b> Last Updated (y-m-d-h:m:s) </b> </td> </tr>"
                    ]
                    for f in glob.iglob(os.path.join(in_path, "*")):
                        stats = os.stat(f)
                        is_file = os.path.isfile(f)
                        f = os.path.relpath(f, self.dir)
                        html_rows.append(
                            f'<tr> <td> <a href="{f}">{os.path.basename(f)}</a> </td> <td> {round(stats.st_size/(1024 * 1024), 6) if is_file else "Directory"}  </td> <td> {datetime.datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d-%H:%M:%S")} </td> </tr>'
                        )

                    resp.content_type = "text/html"
                    resp.text = f"<!DOCTYPE html> <html> <body> <h2>Files:</h2> <table style='border-spacing: 0 1em;width:80%;margin-left:auto;margin-right:auto'> {' '.join(html_rows)} </table> </body> </html>"

            else:
                if not os.path.exists(in_path):
                    resp.media = falcon.HTTP_404

                else:
                    resp.content_type = mimetypes.guess_type(in_path, strict=False)[0]
                    if resp.content_type is None:
                        resp.content_type = "text/plain"

                    # resp.downloadable_as = os.path.basename(in_path)

                    resp.stream = open(in_path, "rb")

        except Exception as ex:
            logging.exception(ex, exc_info=True)
            resp.media = str(ex)
            resp.status = falcon.HTTP_400


def _main(
    host="0.0.0.0",
    port=8080,
    public=False,
    no_index=False,
    no_symlinks=False,
    dir="./",
    username=None,
    password=None,
):
    app = falcon.App(cors_enable=True)
    app.req_options.auto_parse_form_urlencoded = True
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
    app = falcon.App(
        middleware=falcon.CORSMiddleware(
            allow_origins=ALLOWED_ORIGINS, allow_credentials=ALLOWED_ORIGINS
        )
    )

    file_server_api = fileServer(dir=dir, no_index=no_index, no_symlinks=no_symlinks)

    app.add_sink(file_server_api.on_get, prefix="/")

    class StandaloneApplication(gunicorn.app.base.BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {
                key: value
                for key, value in self.options.items()
                if key in self.cfg.settings and value is not None
            }
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    WORKERS = 1

    WORKERS = int(os.getenv("WORKERS", "1"))

    options = {
        "preload": True,
        "bind": "%s:%s" % (host, port),
        "workers": WORKERS,
        "worker_connections": 1000,
        "worker_class": "gevent",
        "timeout": 300,
        "loglevel": "ERROR",
    }

    cloudflared_process = None
    cloudflared_url = None
    if public:
        # https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz
        logging.info(f"Establishing tunnel")
        with tempfile.NamedTemporaryFile() as tmp:
            cloudflared_process = gevent.subprocess.Popen(
                [
                    "cloudflared",
                    "tunnel",
                    "--url",
                    f"localhost:{port}",
                    "--logfile",
                    tmp.name,
                ],
                close_fds=True,
                stdin=gevent.subprocess.DEVNULL,
                stdout=gevent.subprocess.DEVNULL,
                stderr=gevent.subprocess.DEVNULL,
            )
            loop_start = time.time()
            while True:
                if time.time() - loop_start >= 15:
                    logging.warning(f"Establishing a tunnel connection failed.")
                    logging.warning(
                        f"Try manually running the following command in a separate terminal."
                    )
                    logging.warning(
                        " ".join(
                            ["cloudflared", "tunnel", "--url", f"localhost:{port}"]
                        )
                    )
                    try:
                        cloudflared_process.kill()
                    except:
                        pass
                    break
                try:
                    cloudflared_url = [
                        _
                        for _ in open(tmp.name).read().split()
                        if _.startswith("https://") and _.endswith(".trycloudflare.com")
                    ][0]
                    break
                except:
                    time.sleep(1)
                    pass

    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == socket.AF_INET:
                rich.print(f"http://{snic.address}:{port}")

    def handle_exit(*args):
        if cloudflared_process is not None:
            logging.info(f"Stopping tunnel")
            cloudflared_process.kill()

    atexit.register(handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)

    if cloudflared_url:
        rich.print(cloudflared_url)

    StandaloneApplication(app, options).run()


def batserve():
    logging.info(f"[yellow]Starting[/yellow] batServe")
    _main(
        host=args.host if args.host else "0.0.0.0",
        port=int(args.port) if args.port and args.port.isdigit() else 8080,
        public=args.public,
        no_index=not args.index,
        no_symlinks=not args.symlinks,
        dir=args.dir if args.dir and os.path.exists(args.dir) else "./",
        username=args.username,
        password=args.password,
    )


if __name__ == "__main__":
    main()
