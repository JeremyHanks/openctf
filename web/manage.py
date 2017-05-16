from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from openctf import create_app
from openctf.models import db

app = create_app()
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

ServerCommand = Server(host="0.0.0.0", port=80, use_debugger=True, use_reloader=True)
manager.add_command("runserver", ServerCommand)

if __name__ == "__main__":
    manager.run()
