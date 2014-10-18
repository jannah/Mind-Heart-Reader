from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
mhreader_experiment_files = Table('mhreader_experiment_files', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('stimulus_type', String),
    Column('title', String),
    Column('filename', String),
    Column('filepath', String),
    Column('file_set_number', Integer),
    Column('male_response', String),
    Column('female_response', String),
    Column('remarks', String),
)

mhreader_experiment_set_files = Table('mhreader_experiment_set_files', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('experiment_set_id', Integer),
    Column('experiment_file_id', Integer),
    Column('order', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mhreader_experiment_files'].columns['female_response'].create()
    post_meta.tables['mhreader_experiment_files'].columns['male_response'].create()
    post_meta.tables['mhreader_experiment_set_files'].columns['order'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mhreader_experiment_files'].columns['female_response'].drop()
    post_meta.tables['mhreader_experiment_files'].columns['male_response'].drop()
    post_meta.tables['mhreader_experiment_set_files'].columns['order'].drop()
