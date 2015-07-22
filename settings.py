import os
import tornado
from tornado.options import define, options


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

define('port', default=8889, help="run on the given port", type=int)
define('debug', default=True, help='debug mode')
tornado.options.parse_command_line()


settings = {}
settings['debug'] = options.debug
settings['static_path'] = os.path.join(BASE_DIR, 'static')
settings['template_path'] = os.path.join(BASE_DIR, 'templates')
settings['cookie_secret'] = os.environ.get('SECRET_TOKEN', '__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__')
settings['xsrf_cookies'] = True
settings['login_url'] = '/auth/login/'

from modules.modules import SearchBar, DeleteModal, CreateModal, EditModal
settings['ui_modules'] = {'SearchBar': SearchBar, 'DeleteModal': DeleteModal,
                          'CreateModal': CreateModal, 'EditModal': EditModal}

DATABASES = {
    'default': {
        'ENGINE': 'postgresql+psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
url_placeholder = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
url = url_placeholder.format(**DATABASES['default'])