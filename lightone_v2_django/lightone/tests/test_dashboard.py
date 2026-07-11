from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from lightone.models import MemberSession
from lightone.services import routing_badge_class, routing_label, trainer_dashboard_context


class DashboardRoutingBadgeTests(TestCase):
    def create_session(self, route, pain_response):
        return MemberSession.objects.create(
            member_name=f'{route}-member',
            goal='routing badge check',
            form_accuracy=90,
            rep_score=90,
            rest_score=90,
            rpe=7,
            pain_response=pain_response,
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
        for route, pain_response in [('AUTO', 1), ('REVIEW', 4), ('BLOCK', 8)]:
            self.create_session(route, pain_response)

        response = self.client.get(reverse('lightone:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'badge-green')
        self.assertContains(response, 'badge-yellow')
        self.assertContains(response, 'badge-red')
        self.assertContains(response, 'report_system_showcase.png')
        self.assertContains(response, 'studio_interior_day.png')
        self.assertContains(response, 'studio_walkthrough.mp4')
        self.assertContains(response, 'studio_exterior.png')
        self.assertContains(response, 'LIGHT ONE PT V1 REPORT SYSTEM')
        self.assertContains(response, 'AI 기반 비의료적 컨디셔닝 케어')

    def test_trainer_dashboard_prioritizes_review_and_block_sessions(self):
        self.create_session('AUTO', 1)
        self.create_session('REVIEW', 4)
        self.create_session('BLOCK', 8)

        context = trainer_dashboard_context()

        self.assertEqual(len(context['review_queue']), 2)
        self.assertEqual(context['counts']['AUTO'], 1)
        self.assertEqual(context['counts']['REVIEW'], 1)
        self.assertEqual(context['counts']['BLOCK'], 1)

    def test_trainer_dashboard_renders_non_medical_review_queue(self):
        user = get_user_model().objects.create_user(
            username='trainer-dashboard-user',
            password='test-pass',
            name='Trainer Dashboard User',
        )
        self.client.force_login(user)
        self.create_session('REVIEW', 5)
        self.create_session('BLOCK', 8)

        response = self.client.get(reverse('lightone:trainer_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Session Workflow')
        self.assertContains(response, 'Today Sessions')
        self.assertContains(response, 'Member Search / List')
        self.assertContains(response, 'Review Queue')
        self.assertContains(response, 'Report Drafts')
        self.assertContains(response, 'Next Session Plan')
        self.assertContains(response, 'studio_interior_evening.png')
        self.assertContains(response, 'LIGHT ONE PT V1 REPORT SYSTEM')
        self.assertContains(response, '트레이너 회원관리 SaaS 서비스')
        self.assertContains(response, '비의료 웰니스 참고 정보')
        self.assertContains(response, 'badge-yellow')
        self.assertContains(response, 'badge-red')

    def test_trainer_dashboard_orders_block_before_review(self):
        self.create_session('REVIEW', 4)
        self.create_session('BLOCK', 8)

        context = trainer_dashboard_context()

        self.assertEqual([session.route for session in context['review_queue']], ['BLOCK', 'REVIEW'])

    def test_login_uses_walkthrough_video_and_canonical_report_system_copy(self):
        response = self.client.get(reverse('accounts:login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'studio_walkthrough.mp4')
        self.assertContains(response, 'report_system_showcase.png')
        self.assertContains(response, 'LIGHT ONE PT')
        self.assertContains(response, 'REPORT SYSTEM')
        self.assertContains(response, '트레이너 회원관리 SaaS 서비스')
        self.assertContains(response, 'AI 기반 비의료적 컨디셔닝 케어')
