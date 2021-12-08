def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="batbelt file utils - rename, move, extract ... files"
    )

    parser.add_argument(
        "--move",
        help="Serve on host. Defaults to 0.0.0.0",
        nargs="?",
    )

    parser.add_argument(
        "--port",
        help="Serve on port. Defaults to 8080",
        nargs="?",
    )

    parser.add_argument(
        "-u",
        "--username",
        help="Username for security, not set by default",
        nargs="?",
    )

    parser.add_argument(
        "-p",
        "--password",
        help="password for security, not set by default",
        nargs="?",
    )

    args = parser.parse_args()
