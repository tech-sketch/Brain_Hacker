# -*- coding: utf-8 -*-
from models.user import User


def check_group_permission(f):
    """
    グループに所属していない場合は、リダイレクトする。
    """
    def wrapper(*args):
        user = args[0].get_current_user()
        if not user:
            args[0].redirect(args[0].reverse_url('login'))
            return
        ##user = args[0].session.query(User).filter_by(id=user['id']).first()
        user = User.get(user['id'])
        if user.belongs_to_group(int(args[1])):
            pass
        else:
            error_message = 'この操作は許可されていません。'
            args[0].redirect(args[0].reverse_url('index') + '?error_message={0}'.format(error_message))
            return
        return f(*args)
    return wrapper