from sqlalchemy import *
import sqlalchemy.ext.declarative
from models.base_model import Base


association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)