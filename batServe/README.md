<p align="center">
    <h1 align="center">batServe</h1>
    <p align="center">simple, useful file server | part of <b><i>batBelt</i></b></p>
</p>


**Installation**:

- If you have python >= 3.6 installed and want to install batServe only

```pip install --upgrade batserve```

- If you don't have python pre-installed, batServe is available as a pre-built binary via batBelt

**Usage**:

```
usage: batserve (or) python -m batserve (optional arguments)

batBelt file server (1.0-rc4) - simple and useful file server

optional arguments:
  -h, --help            show this help message and exit
  --host [HOST]         Serve on host (eg: localhost, 0.0.0.0). Defaults to 0.0.0.0
  --port [PORT]         Serve on port. Defaults to 8080
  --public              Serve on a publicly accessible URL
  --no-index            Disable auto-generation of index.html
  --no-symlinks         Don't follow symlinks
  --dir [DIR]           The directory path to serve. Defaults to ./
  -u [USERNAME], --username [USERNAME]
                        Username for security, not set by default
  -p [PASSWORD], --password [PASSWORD]
                        Password for security, not set by default

```
