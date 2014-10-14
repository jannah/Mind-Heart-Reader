from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
mhreader_experiment_logs = Table('mhreader_experiment_logs', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('experiment_id', INTEGER),
    Column('action', INTEGER),
    Column('timestamp', DATETIME),
    Column('action_type', VARCHAR),
    Column('experiment_set_file_id', INTEGER),
    Column('result', VARCHAR),
)

mhreader_experiment_logs = Table('mhreader_experiment_logs', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('experiment_id', Integer),
    Column('action', Integer),
    Column('timestamp', DateTime),
    Column('action_type', String),
    Column('experiment_file_id', Integer),
    Column('result', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['mhreader_experiment_logs'].columns['experiment_set_file_id'].drop()
    post_meta.tables['mhreader_experiment_logs'].columns['experiment_file_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['mhreader_experiment_logs'].columns['experiment_set_file_id'].create()
    post_meta.tables['mhreader_experiment_logs'].columns['experiment_file_id'].drop()
