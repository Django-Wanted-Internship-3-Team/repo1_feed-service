from django.urls import reverse
from rest_framework.test import APITestCase


class SharesAPITestCase(APITestCase):
    """
    /shares/<content_id>/ post 에 대한 테스트 케이스
    """

    viewname = "shares"

    def test_post_failure_no_api(self):
        path = reverse(self.viewname, kwargs={"content_id": None})
