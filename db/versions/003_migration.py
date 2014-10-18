from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
mhreader_experiment_set_files = Table('mhreader_experiment_set_files', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('experiment_set_id', INTEGER),
    Column('experiment_file_id', INTEGER),
    Column('order', INTEGER),
)

mhreader_experiment_set_files = Table('mhreader_experiment_set_files', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('experiment_set_id', Integer),
    Column('experiment_file_id', Integer),
    Column('experiment_file_order', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['mhreader_experiment_set_files'].columns['order'].drop()
    post_meta.tables['mhreader_experiment_set_files'].columns['experiment_file_order'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['mhreader_experiment_set_files'].columns['order'].create()
    post_meta.tables['mhreader_experiment_set_files'].columns['experiment_file_order'].drop()
