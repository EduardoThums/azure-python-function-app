# from cwipersistence import Transaction, update_transactional, insert_autocommit
from importlib import import_module

# from migrations import migrate
from os import environ
from sys import argv
# from cwiadmin.menu_setup import insert_authorization

environ["APP_CONFIG_FILE"] = "../config/development.py"


app_to_run = environ.get("COCA_APP")
recreate_database = False
port = 5000

if not app_to_run:
    app_to_run = argv[1]

if len(argv) >= 3:
    recreate_database = True if argv[2] == "recreate_database" else False


def create_app():
    global port
    app = import_module(f"{app_to_run}.app").app

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config.get("DEBUG"), port=port)
