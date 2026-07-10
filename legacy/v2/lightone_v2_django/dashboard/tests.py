from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from lightone.models import Indicator, Member, Session


class DashboardPrivacyAndContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.member = Member.objects.create(
            gender=Member.GENDER_OTHER,
            age_group='30s',
            goals='synthetic mobility goal',
            consent=True,
        )
        statuses = [
            Indicator.ROUTING_AUTO,
            Indicator.ROUTING_REVIEW,
            Indicator.ROUTING_BLOCK,
        ]
        for index, status in enumerate(statuses):
            session = Session.objects.create(
                member=cls.member,
                date=timezone.now() - timezone.timedelta(days=2 - index),
                exercise_name=f'synthetic squat pattern {index}',
                sets=3,
                reps_target=10,
                reps_completed=8 + index,
                rpe=6 + index,
                pain_response=index,
                trainer_notes='synthetic non-medical note',
            )
            Indicator.objects.create(
                session=session,
                qs_score=92 - (index * 18),
                form_accuracy=0.90 - (index * 0.10),
                rep_rate=0.80 - (index * 0.05),
                rest_compliance=0.85 - (index * 0.05),
                pain_score=0.10 + (index * 0.30),
                jatc_pain=0.20 + index,
                jatc_posture=0.30 + index,
                jatc_function=0.40 + index,
                jatc_lifestyle=0.50 + index,
                routing_status=status,
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
        response = self.client.get('/dashboard/', {'member_id': self.member.member_id})
        self.assertEqual(response.status_code, 200)

    def test_selected_member_context_contains_dashboard_data(self):
        response = self.client.get(reverse('dashboard'), {'member_id': self.member.member_id})
        self.assertEqual(response.context['selected_member_id'], str(self.member.member_id))
        self.assertIn('qs_labels', response.context)
        self.assertIn('qs_scores', response.context)
        self.assertIn('breakdown_values', response.context)
        self.assertIn('recent_sessions', response.context)
        self.assertEqual(len(response.context['qs_labels']), 3)
        self.assertEqual(len(response.context['qs_scores']), 3)
        self.assertEqual(len(response.context['breakdown_values']), 8)
        self.assertEqual(len(response.context['recent_sessions']), 3)

    def test_dashboard_renders_safety_copy_without_pii(self):
        response = self.client.get('/dashboard/', {'member_id': self.member.member_id})
        html = response.content.decode('utf-8')
        self.assertContains(response, '진단·치료 목적이 아니라 PT 상담과 웰니스 피드백을 위한 프로토타입')
        forbidden_context_keys = {'name', 'phone', 'email', 'address', 'birth_date', 'date_of_birth'}
        context_keys = set()
        for rendered_context in response.context:
            if hasattr(rendered_context, 'flatten'):
                context_keys.update(rendered_context.flatten().keys())
        self.assertTrue(forbidden_context_keys.isdisjoint(context_keys))
        for forbidden in ['이름', '전화번호', '이메일', '주소', '생년월일', '홍길동', '010-1234-5678', 'member@example.test', '서울시 개인정보로', '1990-01-01']:
            self.assertNotIn(forbidden, html)

    def test_dashboard_renders_status_badge_classes(self):
        response = self.client.get('/dashboard/', {'member_id': self.member.member_id})
        self.assertContains(response, 'badge-auto badge-green')
        self.assertContains(response, 'badge-review badge-yellow')
        self.assertContains(response, 'badge-block badge-red')

    def test_font_family_fallback_stack_exists_in_css(self):
        from pathlib import Path
        css_text = Path(__file__).resolve().parents[1].joinpath('static/lightone/css/lightone.css').read_text(encoding='utf-8')
        self.assertIn('font-family: Inter, "Noto Sans KR", "Pretendard", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;', css_text)
