#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import uvicorn


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?") from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1] == "runasync":
            url_args = sys.argv[2].split(":")
            if len(url_args) == 1:
                url_args.append("8000")
            if url_args[0] == "":
                url_args[0] = "127.0.0.1"
            if not url_args[1].isdigit():
                url_args[1] = "8000"
            uvicorn.run("mysite.asgi:application",
                        host=url_args[0],
                        port=int(url_args[1]),
                        log_level="info")
        else:
            main()
    else:
        main()
