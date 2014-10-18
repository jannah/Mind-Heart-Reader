from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
mhreader_experiments = Table('mhreader_experiments', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String),
    Column('user_id', Integer),
    Column('experiment_set_id', Integer),
    Column('remarks', String),
    Column('start_time', DateTime),
    Column('end_time', DateTime),
    Column('completed', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mhreader_experiments'].columns['completed'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mhreader_experiments'].columns['completed'].drop()
