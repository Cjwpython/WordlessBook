# coding: utf-8
from flask_script import Manager, Server
from apps import app

manager = Manager(app)
manager.add_command("runserver",
                    Server(host='0.0.0.0',
                           port=app.config['SERVER_PORT'],
                           use_debugger=app.config["USER_DEBUG"],
                           use_reloader=app.config["USER_RELOAD"],
                           threaded=True)
                    )

if __name__ == "__main__":
    print(app.url_map)
    manager.run()
