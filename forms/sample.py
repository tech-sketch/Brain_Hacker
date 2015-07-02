# -*- coding: utf-8 -*-
import os
import sys
my_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(my_dir, '..')))

import tornado.ioloop
import tornado.web

from wtforms.fields import IntegerField
from wtforms.validators import DataRequired
from wtforms_tornado import Form


import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from wtforms_alchemy import ModelForm

engine = create_engine('sqlite:///:memory:')
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Sum(Base):
    __tablename__ = 'sum'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    a = sa.Column(sa.Integer, nullable=False)
    b = sa.Column(sa.Integer, nullable=False)


from models.user import User
class UserForm(ModelForm, Form):
    class Meta:
        model = User


class SumForm(ModelForm, Form):
    class Meta:
        model = Sum
"""
class SumForm(Form):
    a = IntegerField(validators=[DataRequired()])
    b = IntegerField(validators=[DataRequired()])
"""
class SumHandler(tornado.web.RequestHandler):

    def get(self):
        sumform = SumForm()
        #fields = [val for val in UserForm()._fields]
        #print(fields)
        #form = UserForm()
        from forms.forms import GroupForm
        form = GroupForm(prefix="test")
        names = [name for name in GroupForm()._fields]
        #form['name'].name = "hello"
        for name in names:
            getattr(form, name).name = name
        #getattr(form, 'name').name = "hello"
        #for field_name in fields:
         #   print(getattr(form, field_name).name)
            #setattr(form, field_name, 'aiueo')
            #print(getattr(form, field_name))
        self.render('test.html', sumform=sumform, user_form=form)

    def post(self):
        form = SumForm(self.request.arguments)
        if form.validate():
            self.write(str(form.data['a'] + form.data['b']))
        else:
            self.set_status(400)
            print("error")
            self.write(form.errors)

application = tornado.web.Application([
    (r"/", SumHandler),],)

if __name__ == "__main__":
    application.listen(8890)
    tornado.ioloop.IOLoop.instance().start()