from django.test import TestCase
from django.utils import timezone

from common.utils import get_before_week, get_now


class DateUtilityTest(TestCase):
    def test_get_now(self):
        now = get_now()
        current_date = timezone.now().strftime("%Y-%m-%d")
        self.assertEqual(now, current_date)

    def test_get_before_week(self):
        before_week = get_before_week()
        expected_date = (timezone.now() - timezone.timedelta(days=7)).strftime("%Y-%m-%d")
        self.assertEqual(before_week, expected_date)
