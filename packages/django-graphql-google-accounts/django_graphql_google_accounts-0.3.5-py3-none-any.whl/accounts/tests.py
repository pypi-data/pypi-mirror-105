from django.test import TestCase
from django.test.client import RequestFactory
from accounts.views import GoogleCallbackView

# Create your tests here.


class GoogleRequestTest(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_callback(self):
        code = '4%2F0AY0e-g51bsMsce_r4V7mWCr_3i4pMFmi2Gsj783R_URUU-VhcJ8SAAlddQPuk7tlcYsQ1Q'
        scope = 'email profile https://www.googleapis.com/auth/userinfo.email openid https://www.googleapis.com/auth/userinfo.profile'
        req = self.factory.get(f'/auth/google/callback?code={code}&scope={scope}&authuser=1&prompt=consent', SERVER_NAME='localhost:8000')
        resp = GoogleCallbackView.as_view()(req)
        self.assertEqual(resp.status_code, 200)
