#!/usr/bin/env python
from commandlinestart import Cli, echo

import uvicorn
import kode as service



def run_server():
    """
    Запуск FastAPI сервера.
    """
    echo("Запуск FastAPI сервера...")
    uvicorn.run("kode:start_app", host="0.0.0.0", port=8000, reload=True, factory=True)


def create_cli():
    cli = Cli(service=service)

    cli.add_command("server", run_server)

    return cli


if __name__ == "__main__":
    cli = create_cli()
    cli.start()
