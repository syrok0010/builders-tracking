#!/usr/bin/python
import os

from typer import Typer

import config
from client import client as client_funcs
from installer import install
from server import deactivated_worker

app = Typer()


@app.command()
def client():
    if os.getuid() != 0:
        print('This script should run with elevated privileges')
        return
    try:
        install('ping', client_funcs.initial_send_hwinfo)
        print('Client is successfully installed')
    except Exception as e:
        print(e)


@app.command()
def ping():
    client_funcs.ping()


@app.command()
def deactivated():
    deactivated_worker.mark_deactivated()


@app.command()
def server():
    try:
        install('deactivated')
        os.system(f'fastapi run server/main.py --port {config.server_port}')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app()
