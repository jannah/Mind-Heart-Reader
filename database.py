# Modified from:
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
import os
import shutil
from sqlalchemy import create_engine
from sys import argv

from app import app
from app import db
from migrate.versioning import api
import imp

SQLALCHEMY_DATABASE_URI = app.config["SQLALCHEMY_DATABASE_URI"]
SQLALCHEMY_MIGRATE_REPO = app.config["SQLALCHEMY_MIGRATE_REPO"]

def create():
    print SQLALCHEMY_DATABASE_URI
    print SQLALCHEMY_MIGRATE_REPO
    create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
            api.version(SQLALCHEMY_MIGRATE_REPO))

def migrate():
    migration = (SQLALCHEMY_MIGRATE_REPO +
        '/versions/%03d_migration.py' % (api.db_version(SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO) + 1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO)
    #FIXME
    exec old_model in tmp_module.__dict__
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('New migration saved as ' + migration)
    print('Current database version: ' +
        str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)))

def upgrade():
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' +
        str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)))

def downgrade():
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
    print('Current database version: ' +
        str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)))

def drop():
    os.remove(SQLALCHEMY_DATABASE_URI.split('///')[-1])
    shutil.rmtree(SQLALCHEMY_MIGRATE_REPO)

def reset():
    # Remove old database if it's there
    try:
        os.remove(SQLALCHEMY_DATABASE_URI.split('///')[-1])
    except OSError:
        print("Database not found; creating new database.")

    db.create_all()

def cache():
    """Copy the current database file to ``SQLALCHEMY_DATABASE_CACHE_PATH``.
    """
    shutil.copyfile(app.config["SQLALCHEMY_DATABASE_PATH"],
        app.config["SQLALCHEMY_DATABASE_CACHE_PATH"])

def restore_cache():
    """Copy the cached file to where the database file should be.
    """
    shutil.copyfile(app.config["SQLALCHEMY_DATABASE_CACHE_PATH"],
        app.config["SQLALCHEMY_DATABASE_PATH"])

def clean():
    """Restore cache and roll back the session.
    """
    restore_cache()
    db.session.rollback()
    db.session.expunge_all()

if __name__ == "__main__":
    if len(argv)==1:
            argv.append(raw_input('enter operation:\n'))
    if argv[1] == "create":
        create()
    elif argv[1] == "migrate":
        migrate()
    elif argv[1] == "upgrade":
        upgrade()
    elif argv[1] == "downgrade":
        downgrade()
    elif argv[1] == "drop":
        drop()
    elif argv[1] == "reset":
        reset()
    else:
        print(str(argv[1]) + " is not a valid database operation.")

