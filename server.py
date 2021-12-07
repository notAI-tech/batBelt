import rich


def get_args():
    import argparse

    class ArgumentParser(argparse.ArgumentParser):
        def _print_message(self, message, file=None):
            rich.print(message)

    parser = ArgumentParser(
        description="[green]batBelt[/green] file server - simple and useful file server"
    )
    parser.add_argument("--host", help="Serve on host (eg: localhost, 0.0.0.0). Defaults to 0.0.0.0", nargs="?")
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

    args = parser.parse_args()

    return args


def start_cloudflared():
    pass


class fileServer(object):
    def __init__(self, dir, no_index, no_symlinks):
        self.dir = dir
        self.no_index = no_index
        self.no_symlinks = no_symlinks
        
    def on_get(self, req, resp):
        try:
            in_path = os.path.join(self.dir, req.relative_uri.strip().lstrip("/"))

            if os.path.isdir(in_path):
                if os.path.exists(os.path.join(in_path, "index.html")):
                    resp.content_type = "text/html"
                    resp.stream = open(os.path.join(in_path, "index.html"), "rb")
                elif self.no_index:
                    resp.media = "inde.html doesn't exist and auto-generation is disabled"
                    resp.status = falcon.HTTP_404
                else:
                    # index_page = epyk.Page()
                    for f in glob.iglob(os.path.join(in_path, '*')):
                        pass
                    resp.media = glob.glob(os.path.join(in_path, '*'))

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


def main(
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

    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")

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

    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == socket.AF_INET:
                rich.print(f"http://{snic.address}:{port}")

    StandaloneApplication(app, options).run()


if __name__ == "__main__":
    args = get_args()

    from gevent import monkey

    monkey.patch_all()

    import os
    import sys
    import glob
    import time
    import uuid
    import epyk
    import gipc
    import falcon
    import gevent
    import shutil
    import psutil
    import socket
    import logging
    import datetime
    import mimetypes
    import gunicorn.app.base
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO, format="%(message)s", handlers=[RichHandler(markup=True)]
    )

    logging.info(f"[yellow]Starting[/yellow] batServe")

    main(
        host=args.host if args.host else "0.0.0.0",
        port=int(args.port) if args.port and args.port.isdigit() else 8080,
        public=args.public,
        no_index=not args.index,
        no_symlinks=not args.symlinks,
        dir=args.dir if args.dir and os.path.exists(args.dir) else "./",
        username=args.username,
        password=args.password,
    )
