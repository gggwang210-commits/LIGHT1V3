from django.test import TestCase

from lightone.algorithms import calculate_qs, determine_routing
from lightone.models import Indicator, MemberSession


class QsCalculatorTests(TestCase):
    def test_synthetic_case_1_qs_about_85_low_pain_routes_auto(self):
        qs_score = calculate_qs(form_accuracy=80, discomfort_response=2, rpe=7, qc_score=90)

        self.assertAlmostEqual(qs_score, 85.0, places=1)
        self.assertEqual(
            determine_routing(qs_score=qs_score, jatc_score=85, discomfort_response=2, qc_status='PASS'),
            'AUTO',
        )

    def test_synthetic_case_2_qs_about_65_routes_review(self):
        qs_score = calculate_qs(form_accuracy=60, discomfort_response=4, rpe=8, qc_score=70)

        self.assertAlmostEqual(qs_score, 67.0, delta=2.0)
        self.assertEqual(
            determine_routing(qs_score=qs_score, jatc_score=65, discomfort_response=3, qc_status='PASS'),
            'REVIEW',
        )

    def test_synthetic_case_3_high_pain_or_safety_flag_routes_block_regardless_of_qs(self):
        qs_score = calculate_qs(form_accuracy=100, discomfort_response=0, rpe=7, qc_score=100)

        self.assertEqual(
            determine_routing(qs_score=qs_score, jatc_score=qs_score, discomfort_response=8, qc_status='PASS'),
            'BLOCK',
        )
        self.assertEqual(
            determine_routing(qs_score=qs_score, jatc_score=qs_score, discomfort_response=1, qc_status='FAIL'),
            'BLOCK',
        )

    def test_membersession_save_creates_and_updates_indicator(self):
        session = MemberSession.objects.create(
            member_name='Synthetic Member Indicator',
            goal='Synthetic QS integration check',
            qs_score=85,
            jatc_score=82,
            route='AUTO',
            posture_score=88,
            lifestyle_score=72,
            function_training_score=91,
            pain_response=1,
            review_note='initial auto route',
            trainer_confirmed=False,
        )

        indicator = Indicator.objects.get(member_session=session)
        self.assertEqual(indicator.qs_score, 85)
        self.assertEqual(indicator.jatc_score, 82)
        self.assertEqual(indicator.review_signal, 'AUTO')
        self.assertEqual(indicator.report_status, 'READY')

        session.qs_score = 35
        session.jatc_score = 38
        session.route = 'BLOCK'
        session.review_note = 'blocked after safety review'
        session.trainer_confirmed = True
        session.save()

        self.assertEqual(Indicator.objects.filter(member_session=session).count(), 1)
        indicator.refresh_from_db()
        self.assertEqual(indicator.qs_score, 35)
        self.assertEqual(indicator.jatc_score, 38)
        self.assertEqual(indicator.review_signal, 'BLOCK')
        self.assertEqual(indicator.report_status, 'HELD')
        self.assertEqual(indicator.review_note, 'blocked after safety review')
        self.assertTrue(indicator.trainer_confirmed)
