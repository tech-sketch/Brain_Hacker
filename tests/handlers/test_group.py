from urllib import parse
from tests.handlers.test_base import TestBase
import re

"""
Test user value
             {
                'username': 'test',
                'email': 'test@test.co.jp',
                'password': 'test'
            }

"""

class TestGroupHandler(TestBase):

    group_id = 0

    def test_groups_get_and_post_request(self):
        test_url = '/groups/'
        response = self.user_login()
        user_cookie = response.headers['Set-Cookie']

        response = self.fetch(test_url,  method='GET', headers={'Cookie': user_cookie})
        # print(response)
        self.assertEqual(response.code, 200)

        post_args = {
            'name': 'test-group',
            'description': 'my test, my life'
        }

        response = self.fetch(test_url,  method='POST', body=parse.urlencode(post_args),
                              follow_redirects=False,  headers={'Cookie': user_cookie})
        print(response)

        self.assertEqual(response.code, 302)
        self.assertTrue(
            str(response.headers['Location']).startswith(r'/groups/'),
            "response.headers['Location'] did not ends with /groups/"
        )

        match = re.findall(r'[0-9]+',response.headers['Location'])
        self.group_id = match[0]
        print(self.group_id)

    def test_group_gett_request(self):
        print(self.group_id)

        test_url = '/groups/' + self.group_id
        response = self.user_login()
        user_cookie = response.headers['Set-Cookie']

        response = self.fetch(test_url,  method='GET', headers={'Cookie': user_cookie})
        # print(response)
        self.assertEqual(response.code, 200)



"""
    def test_get_and_post_request_before_login(self):
        # Bad Request
        test_url = '/groups/'

        response = self.fetch(test_url,  method='GET', follow_redirects=False)
        print(response)
        self.assertEqual(response.code, 302)
        self.assertTrue(
            response.headers['Location'].startswith('/auth/login/'),
            "response.headers['Location'] did not ends with /auth/login/"
        )

        response = self.fetch(test_url,  method='POST', body=parse.urlencode(self.post_args), follow_redirects=False)
        print(response)

        self.assertEqual(response.code, 302)
        self.assertTrue(
            response.headers['Location'].startswith('/auth/login/'),
            "response.headers['Location'] did not ends with /auth/login/"
        )
"""

