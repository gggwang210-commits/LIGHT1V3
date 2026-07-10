from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from lightone.models import Member, MemberSession


class DashboardPrivacyAndContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.member = Member.objects.create(
            synthetic_id='synthetic-member-a',
            display_label='Synthetic Member A',
            goal='synthetic mobility goal',
            discomfort_area='shoulder',
            consent_status='synthetic_demo',
        )
        for index, route in enumerate(['AUTO', 'REVIEW', 'BLOCK']):
            MemberSession.objects.create(
                member_name=cls.member.display_label,
                goal=cls.member.goal,
                discomfort_area=cls.member.discomfort_area,
                qs_score=92 - (index * 18),
                jatc_score=90 - (index * 15),
                form_accuracy=90 - (index * 10),
                rep_score=80 - (index * 5),
                rest_score=85 - (index * 5),
                pain_response=index,
                rpe=6 + index,
                route=route,
                qc_status='PASS',
                memo='synthetic non-medical note',
            )
        User = get_user_model()
        cls.user = User.objects.create_user(
            username='synthetic_trainer',
            email='synthetic-trainer@example.test',
            password='test-pass-1234',
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_dashboard_url_returns_200_for_selected_member(self):
        response = self.client.get('/dashboard/', {'member_id': self.member.synthetic_id})
        self.assertEqual(response.status_code, 200)

    def test_selected_member_context_contains_dashboard_data(self):
        response = self.client.get(reverse('dashboard'), {'member_id': self.member.synthetic_id})
        self.assertEqual(response.context['selected_member_id'], self.member.synthetic_id)
        self.assertIn('qs_labels', response.context)
        self.assertIn('qs_scores', response.context)
        self.assertIn('breakdown_values', response.context)
        self.assertIn('recent_sessions', response.context)
        self.assertEqual(len(response.context['qs_labels']), 3)
        self.assertEqual(len(response.context['qs_scores']), 3)
        self.assertEqual(len(response.context['breakdown_values']), 8)
        self.assertEqual(len(response.context['recent_sessions']), 3)

    def test_dashboard_context_excludes_direct_pii_keys(self):
        response = self.client.get('/dashboard/', {'member_id': self.member.synthetic_id})
        html = response.content.decode('utf-8')
        forbidden_context_keys = {'name', 'phone', 'email', 'address', 'birth_date', 'date_of_birth'}
        context_keys = set()
        for rendered_context in response.context:
            if hasattr(rendered_context, 'flatten'):
                context_keys.update(rendered_context.flatten().keys())
        self.assertTrue(forbidden_context_keys.isdisjoint(context_keys))
        for forbidden in ['010-1234-5678', 'member@example.test', '1990-01-01']:
            self.assertNotIn(forbidden, html)

    def test_dashboard_renders_status_badge_classes(self):
        response = self.client.get('/dashboard/', {'member_id': self.member.synthetic_id})
        self.assertContains(response, 'badge-auto badge-green')
        self.assertContains(response, 'badge-review badge-yellow')
        self.assertContains(response, 'badge-block badge-red')

    def test_font_family_fallback_stack_exists_in_css(self):
        from pathlib import Path

        css_text = Path(__file__).resolve().parents[1].joinpath('static/lightone/css/lightone.css').read_text(encoding='utf-8')
        self.assertIn('--font-dashboard:', css_text)
        self.assertIn('"Noto Sans KR"', css_text)
        self.assertIn('font-family: var(--font-dashboard);', css_text)
