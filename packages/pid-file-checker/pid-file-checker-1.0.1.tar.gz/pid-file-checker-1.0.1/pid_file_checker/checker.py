import logging
from argparse import ArgumentParser
from pathlib import Path

import psutil

from pid_file_checker.exceptions import InvalidPidError

logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser(
        description="Check for the presence of a pid file. "
        "The file must contain one and only one integer "
        "which must be the pid of a running process. "
        "Otherwise, return a code != 0. "
        "Meant to be used in a healthcheck context like with Docker or Kubernetes.",
        epilog="Brought to you by IT4NW@ITSF.",
    )
    parser.add_argument(
        "pid_file",
        help="The pid file you want to monitor",
    )
    args = parser.parse_args()
    pid_file = Path(args.pid_file)
    checker(pid_file)


def checker(pid_file: Path):
    if not pid_file.is_file():
        raise FileNotFoundError("Celery beat is not running yet")

    content = pid_file.read_text()
    try:
        pid = int(content)
    except ValueError:
        raise InvalidPidError("Found pid file but content is not an integer")

    if psutil.pid_exists(pid):
        logger.info("Celery beat is alive at pid %s", pid)
    else:
        raise InvalidPidError(f"Found pid file but content is not a pid: {pid}")


if __name__ == "__main__":
    main()
