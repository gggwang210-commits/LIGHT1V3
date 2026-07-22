import os
import secrets

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.models import MemberProfile, TrainerProfile, User
from lightone.models import MemberSession, StrategyItem


PASSWORD_ENV_NAMES = {
    'syn-admin': 'LIGHTONE_DEMO_ADMIN_PASSWORD',
    'syn-001': 'LIGHTONE_DEMO_MEMBER_A_PASSWORD',
    'syn-002': 'LIGHTONE_DEMO_MEMBER_B_PASSWORD',
}
DISALLOWED_DEMO_PASSWORDS = {'password', 'password123', 'qwerty1234'}


class Command(BaseCommand):
    help = 'Create local-only synthetic LIGHT ONE demo data and accounts.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--generate-passwords',
            action='store_true',
            help='Generate one-time demo passwords and print them to this terminal.',
        )

    def _passwords(self, generate):
        passwords = {}
        missing = []

        for username, env_name in PASSWORD_ENV_NAMES.items():
            value = os.environ.get(env_name, '').strip()
            if not value and generate:
                value = secrets.token_urlsafe(18)
            if not value:
                missing.append(env_name)
                continue
            if len(value) < 12 or value.lower() in DISALLOWED_DEMO_PASSWORDS:
                raise CommandError(
                    f'{env_name} must be at least 12 characters and not a common password.'
                )
            passwords[username] = value

        if missing:
            raise CommandError(
                'Set all demo password environment variables or rerun with '
                f'--generate-passwords. Missing: {", ".join(missing)}'
            )
        return passwords

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError(
                'seed_lightone is disabled when DEBUG=False. '
                'Use mysite.settings_local and explicitly set DEBUG=True.'
            )

        generated = options['generate_passwords']
        passwords = self._passwords(generated)

        trainer_user, _ = User.objects.get_or_create(
            username='syn-admin',
            defaults={
                'email': 'syn-admin@example.invalid',
                'name': '데모관리자',
                'role': 'trainer',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        trainer_user.email = 'syn-admin@example.invalid'
        trainer_user.name = '데모관리자'
        trainer_user.role = 'trainer'
        trainer_user.is_staff = True
        trainer_user.is_superuser = True
        trainer_user.set_password(passwords['syn-admin'])
        trainer_user.save()

        trainer_profile, _ = TrainerProfile.objects.get_or_create(
            user=trainer_user,
            defaults={
                'certification_no': 'SYN-TR-001',
                'center_name': '데모센터-A',
            },
        )
        trainer_profile.certification_no = 'SYN-TR-001'
        trainer_profile.center_name = '데모센터-A'
        trainer_profile.save()

        member_specs = [
            (
                'syn-001',
                'syn-001@example.invalid',
                '데모회원-A',
                'F',
                '상체 움직임 기록 및 체력 증진',
            ),
            (
                'syn-002',
                'syn-002@example.invalid',
                '데모회원-B',
                'M',
                '하체 움직임 기록 및 근력 강화',
            ),
        ]
        member_profiles = {}
        for username, email, name, sex, goals in member_specs:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'name': name, 'role': 'member'},
            )
            user.email = email
            user.name = name
            user.role = 'member'
            user.is_staff = False
            user.is_superuser = False
            user.set_password(passwords[username])
            user.save()
            profile, _ = MemberProfile.objects.get_or_create(user=user)
            profile.sex = sex
            profile.goals = goals
            profile.save()
            member_profiles[name] = profile

        MemberSession.objects.all().delete()
        StrategyItem.objects.all().delete()

        sessions = [
            {'member_name': 'SYN-101', 'goal': '체형 변화 기록', 'discomfort_area': '목·어깨', 'qs_score': 72.4, 'jatc_score': 68.0, 'form_accuracy': 79, 'pain_response': 2, 'rpe': 6, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': '합성 기록. 촬영 조건 양호.'},
            {'member_name': 'SYN-102', 'goal': '하체 컨디셔닝 기록', 'discomfort_area': '무릎', 'qs_score': 63.2, 'jatc_score': 61.5, 'form_accuracy': 70, 'pain_response': 4, 'rpe': 7, 'route': 'REVIEW', 'qc_status': 'CHECK', 'memo': '합성 기록. 담당 트레이너 재확인 필요.'},
            {'member_name': 'SYN-103', 'goal': '러닝 동작 기록', 'discomfort_area': '허리', 'qs_score': 81.5, 'jatc_score': 74.3, 'form_accuracy': 86, 'pain_response': 1, 'rpe': 5, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': '합성 기록. 전후 비교 예시.'},
            {'member_name': 'SYN-104', 'goal': '상체 안정화 기록', 'discomfort_area': '손목', 'qs_score': 49.0, 'jatc_score': 44.6, 'form_accuracy': 50, 'pain_response': 7, 'rpe': 8, 'route': 'BLOCK', 'qc_status': 'FAIL', 'memo': '합성 기록. 운동을 보류하고 담당 트레이너가 재확인.'},
            {'member_name': 'SYN-105', 'goal': '운동 지속 기록', 'discomfort_area': '없음', 'qs_score': 67.5, 'jatc_score': 66.1, 'form_accuracy': 74, 'pain_response': 2, 'rpe': 7, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': '합성 기록. 상담 화면 예시.'},
            {'member_name': 'SYN-106', 'goal': '운동 습관 기록', 'discomfort_area': '어깨', 'qs_score': 58.2, 'jatc_score': 55.9, 'form_accuracy': 63, 'pain_response': 5, 'rpe': 8, 'route': 'REVIEW', 'qc_status': 'CHECK', 'memo': '합성 기록. RPE와 불편 반응 재확인.'},
            {'member_name': '데모회원-A', 'goal': '상체 후면 움직임 기록', 'discomfort_area': '오른쪽 어깨', 'qs_score': 83.0, 'jatc_score': 72.0, 'form_accuracy': 80, 'pain_response': 3, 'rpe': 6, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': 'SYN-001 계정에 연결된 합성 예시.'},
            {'member_name': '데모회원-B', 'goal': '하체 움직임 기록', 'discomfort_area': '허리 하단', 'qs_score': 52.0, 'jatc_score': 50.0, 'form_accuracy': 55, 'pain_response': 6, 'rpe': 8, 'route': 'REVIEW', 'qc_status': 'CHECK', 'memo': 'SYN-002 계정에 연결된 합성 예시.'},
        ]
        for item in sessions:
            MemberSession.objects.create(
                **item,
                member=member_profiles.get(item['member_name']),
                trainer=trainer_profile,
                trainer_name=trainer_user.name,
            )

        strategies = [
            {'title': '고객 인터뷰 질문지 작성', 'category': '고객검증', 'priority': '높음', 'status': '대기', 'output': '센터 운영자와 트레이너 대상 인터뷰 질문지', 'risk': '지인 중심 인터뷰는 편향 가능'},
            {'title': '센터 파일럿 제안서 작성', 'category': '고객검증', 'priority': '높음', 'status': '대기', 'output': '1~2개 센터 대상 파일럿 제안서', 'risk': '실제 회원 이미지·민감정보 수집 금지'},
            {'title': '수익모델 가설표 작성', 'category': '사업계획서', 'priority': '보통', 'status': '대기', 'output': '월 구독과 옵션별 가격 가설표', 'risk': '미검증 가격을 확정처럼 쓰면 감점'},
        ]
        for item in strategies:
            StrategyItem.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('Synthetic local demo data created.'))
        if generated:
            self.stdout.write('One-time local credentials (do not commit or share):')
            for username, password in passwords.items():
                self.stdout.write(f'  {username}: {password}')
        else:
            self.stdout.write('Passwords were read from environment variables and not printed.')
