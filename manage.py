# -*- coding: utf-8 -*-
from flask_migrate import MigrateCommand
from flask_script.commands import Server, Clean
from flask_script import Manager

from mipres_app.mipres import create_app

app = create_app(debug=True)

manager = Manager(app)

manager.add_command("runserver", Server(threaded=True))
manager.add_command("clean", Clean())
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
