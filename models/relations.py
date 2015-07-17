from sqlalchemy import *
import sqlalchemy.ext.declarative
from models.base_model import Base


association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)


user_idea_association_table = Table('user_idea_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('idea_id', Integer, ForeignKey('idea.id'))
)