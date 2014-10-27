from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
mhreader_mindwave_logs = Table('mhreader_mindwave_logs', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('index', Integer),
    Column('experiment_id', Integer),
    Column('timestamp', DateTime(timezone=True)),
    Column('attention', Float),
    Column('meditation', Float),
    Column('familiarity', Float),
    Column('mental_effort', Float),
    Column('appreciation', Float),
    Column('signal_quality', Integer),
    Column('evant_tagger', Integer),
    Column('delta', Float),
    Column('theta', Float),
    Column('alpha', Float),
    Column('beta', Float),
    Column('gamma', Float),
    Column('response', String),
    Column('new_image', Boolean),
    Column('image_order', Integer),
    Column('image_order_index', Integer),
    Column('experiment_file_id', Integer),
    Column('experiment_log_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mhreader_mindwave_logs'].columns['experiment_file_id'].create()
    post_meta.tables['mhreader_mindwave_logs'].columns['experiment_log_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mhreader_mindwave_logs'].columns['experiment_file_id'].drop()
    post_meta.tables['mhreader_mindwave_logs'].columns['experiment_log_id'].drop()
