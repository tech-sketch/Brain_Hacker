from wtforms_tornado import Form
from wtforms_alchemy import ModelForm

from models.user import User
from models.group import Group
from models.room import Room


class UserForm(ModelForm, Form):
    class Meta:
        model = User


class GroupForm(ModelForm, Form):
    class Meta:
        model = Group


class RoomForm(ModelForm, Form):
    class Meta:
        model = Room