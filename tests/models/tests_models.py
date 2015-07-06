import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base_model import Base
from models.user import User
from models.group import Group
from models.room import Room

class UserTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = sessionmaker(self.engine)()
        Base.metadata.create_all(self.engine)
        self.user = User(name='yamada', email='yamada.tarou@tis.co.jp', password='yamada')
        self.session.add(self.user)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_query_user(self):
        expected = [self.user]
        result = self.session.query(User).all()
        self.assertEqual(result, expected)


class GroupTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = sessionmaker(self.engine)()
        Base.metadata.create_all(self.engine)
        self.group = Group(name='group1', description='This is an example description.')
        self.session.add(self.group)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_query_group(self):
        expected = [self.group]
        result = self.session.query(Group).all()
        self.assertEqual(result, expected)


class RoomTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = sessionmaker(self.engine)()
        Base.metadata.create_all(self.engine)
        self.room = Room(name='room1', theme='This is an example theme.')
        self.session.add(self.room)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_query_room(self):
        expected = [self.room]
        result = self.session.query(Room).all()
        self.assertEqual(result, expected)