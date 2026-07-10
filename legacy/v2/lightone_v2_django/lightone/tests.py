from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import MemberSession
from .services import routing_badge_class, routing_label


class DashboardRoutingBadgeTests(TestCase):
    def create_session(self, route):
        return MemberSession.objects.create(
            member_name=f'{route}-member',
            goal='routing badge check',
            route=route,
            qc_status='PASS',
        )

    def test_routing_badge_helper_normalizes_known_and_unknown_values(self):
        cases = {
            'AUTO': ('AUTO', 'badge-green'),
            'GREEN': ('GREEN', 'badge-green'),
            'Green': ('Green', 'badge-green'),
            'REVIEW': ('REVIEW', 'badge-yellow'),
            'YELLOW': ('YELLOW', 'badge-yellow'),
            'Yellow': ('Yellow', 'badge-yellow'),
            'BLOCK': ('BLOCK', 'badge-red'),
            'RED': ('RED', 'badge-red'),
            'Red': ('Red', 'badge-red'),
            'UNKNOWN': ('UNKNOWN', 'badge-gray'),
        }

        for route, (expected_label, expected_class) in cases.items():
            with self.subTest(route=route):
                self.assertEqual(routing_label(route), expected_label)
                self.assertEqual(routing_badge_class(route), expected_class)

    def test_dashboard_renders_badge_class_for_each_routing_status(self):
        user = get_user_model().objects.create_user(
            username='dashboard-user',
            password='test-pass',
            name='Dashboard User',
        )
        self.client.force_login(user)
        for route in ['AUTO', 'GREEN', 'Green', 'REVIEW', 'YELLOW', 'Yellow', 'BLOCK', 'RED', 'Red', 'UNKNOWN']:
            self.create_session(route)

        response = self.client.get(reverse('lightone:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'badge-green')
        self.assertContains(response, 'badge-yellow')
        self.assertContains(response, 'badge-red')
        self.assertContains(response, 'badge-gray')
