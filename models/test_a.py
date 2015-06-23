# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
import sqlalchemy.ext.declarative
Base = sqlalchemy.ext.declarative.declarative_base()


association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    hashed_password = Column(Binary)
    children = relationship("Group", secondary=association_table, backref='users')

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)


DATABASES = {
    'default': {
        'ENGINE': 'postgresql+psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'psobbst5',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
url_placeholder = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
url = url_placeholder.format(**DATABASES['default'])
engine = sqlalchemy.create_engine(url, echo=False)
# スキーマ再構成
Base.metadata.drop_all(engine)
"""
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
import bcrypt
user1 = User(name="name", email="neko@tis.co.jp", hashed_password=bcrypt.hashpw("neko".encode("utf-8"), bcrypt.gensalt()))
user2 = User(name="name", email="nuko@tis.co.jp", hashed_password=bcrypt.hashpw("neko".encode("utf-8"), bcrypt.gensalt()))
group = Group(name="group1")
user1.children = [group, Group(name="group2")]
user2.children = [group, Group(name="group3"), Group(name="group4")]
session.add(user1)
session.add(user2)
session.commit()

parents = session.query(User)
for parent in parents:
    print(parent)
    print(parent.children)
    for group in parent.children:
        print(group.id,)
    print()
group = session.query(Group).filter(Group.id==1).first()
print(dir(group))
print(group.users)
for parent in group.users:
    print(parent.id)
#print(dir(child))
#print(child.parent)"""