from django.core.management.base import BaseCommand

from accounts.models import MemberProfile, TrainerProfile, User
from lightone.models import MemberSession, StrategyItem


class Command(BaseCommand):
    help = 'Create LIGHT ONE premium dashboard demo data and login accounts.'

    def handle(self, *args, **options):
        trainer_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'name': '김라이트(관리자)',
                'role': 'trainer',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        trainer_user.email = 'admin@example.com'
        trainer_user.name = '김라이트(관리자)'
        trainer_user.role = 'trainer'
        trainer_user.is_staff = True
        trainer_user.is_superuser = True
        trainer_user.set_password('admin')
        trainer_user.save()

        trainer_profile, _ = TrainerProfile.objects.get_or_create(
            user=trainer_user,
            defaults={
                'certification_no': 'TR-2026-001',
                'center_name': 'LIGHT ONE 랩스',
            },
        )
        trainer_profile.certification_no = 'TR-2026-001'
        trainer_profile.center_name = 'LIGHT ONE 랩스'
        trainer_profile.save()

        member_specs = [
            ('member1', 'm1@example.com', '이슬비', 'F', '라운드숄더 개선 및 체력 증진'),
            ('member2', 'm2@example.com', '허병철', 'M', '허리 통증 완화 및 근력 강화'),
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
            user.set_password('1234')
            user.save()
            profile, _ = MemberProfile.objects.get_or_create(user=user)
            profile.sex = sex
            profile.goals = goals
            profile.save()
            member_profiles[name] = profile

        MemberSession.objects.all().delete()
        StrategyItem.objects.all().delete()

        sessions = [
            {'member_name': '김도윤', 'goal': '체형 변화 기록 및 재등록 상담', 'discomfort_area': '목·어깨', 'qs_score': 72.4, 'jatc_score': 68.0, 'form_accuracy': 79, 'pain_response': 2, 'rpe': 6, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': '상담 리포트 자동 생성 가능. 촬영 조건 양호.'},
            {'member_name': '이서연', 'goal': '하체 근력 컨디셔닝 및 운동 지속', 'discomfort_area': '무릎', 'qs_score': 63.2, 'jatc_score': 61.5, 'form_accuracy': 70, 'pain_response': 4, 'rpe': 7, 'route': 'REVIEW', 'qc_status': 'CHECK', 'memo': '통증 반응 기록이 있어 트레이너 검토 권장.'},
            {'member_name': '박민준', 'goal': '러닝 자세 개선', 'discomfort_area': '허리', 'qs_score': 81.5, 'jatc_score': 74.3, 'form_accuracy': 86, 'pain_response': 1, 'rpe': 5, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': '전후 비교 리포트에 적합.'},
            {'member_name': '최하린', 'goal': '상체 안정화 루틴', 'discomfort_area': '손목', 'qs_score': 49.0, 'jatc_score': 44.6, 'form_accuracy': 50, 'pain_response': 7, 'rpe': 8, 'route': 'BLOCK', 'qc_status': 'FAIL', 'memo': '통증 반응이 높아 운동 중단 및 전문가 상담 권고 문구 필요.'},
            {'member_name': '정유찬', 'goal': '바디프로필 준비 관리', 'discomfort_area': '없음', 'qs_score': 67.5, 'jatc_score': 66.1, 'form_accuracy': 74, 'pain_response': 2, 'rpe': 7, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': '상담 자료로 사용 가능.'},
            {'member_name': '오지민', 'goal': '운동 습관 형성', 'discomfort_area': '어깨', 'qs_score': 58.2, 'jatc_score': 55.9, 'form_accuracy': 63, 'pain_response': 5, 'rpe': 8, 'route': 'REVIEW', 'qc_status': 'CHECK', 'memo': 'RPE와 통증 반응 확인 필요.'},
            {'member_name': '이슬비', 'goal': '상체 후면 근력 강화', 'discomfort_area': '오른쪽 어깨', 'qs_score': 83.0, 'jatc_score': 72.0, 'form_accuracy': 80, 'pain_response': 3, 'rpe': 6, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': '견갑골 안정화 양호. 회원 계정 member1과 연결된 샘플.'},
            {'member_name': '허병철', 'goal': '하체 근력 및 허리 안정화', 'discomfort_area': '허리 하단', 'qs_score': 52.0, 'jatc_score': 50.0, 'form_accuracy': 55, 'pain_response': 6, 'rpe': 8, 'route': 'REVIEW', 'qc_status': 'CHECK', 'memo': '가동범위 제한 및 코어 안정화 우선. 회원 계정 member2와 연결된 샘플.'},
        ]
        for item in sessions:
            MemberSession.objects.create(
                **item,
                member=member_profiles.get(item['member_name']),
                trainer=trainer_profile,
                trainer_name=trainer_user.name,
            )

        strategies = [
            {'title': '고객 인터뷰 질문지 작성', 'category': '고객검증', 'priority': '높음', 'status': '대기', 'output': 'PT샵 대표, 헬스장 대표, 트레이너 대상 인터뷰 질문지', 'risk': '지인 중심 인터뷰는 편향 가능'},
            {'title': 'PT샵 파일럿 제안서 작성', 'category': '고객검증', 'priority': '높음', 'status': '대기', 'output': '1~2개 센터 대상 파일럿 제안서', 'risk': '실제 회원 이미지·민감정보 수집 금지'},
            {'title': '수익모델 가설표 작성', 'category': '사업계획서', 'priority': '보통', 'status': '대기', 'output': '센터 월 구독, 트레이너 계정 추가, 리포트 저장 옵션별 가격 가설표', 'risk': '미검증 가격을 확정처럼 쓰면 감점'},
            {'title': '촬영 QC 기술 재배치', 'category': 'GitHub / 사업계획서', 'priority': '높음', 'status': '완료', 'output': '촬영 QC·카메라 보정·조명 정규화를 리포트 신뢰도 보조 기술로 재정의', 'risk': '기술이 서비스 주인공처럼 보이지 않게 유지'},
            {'title': 'GitHub 첫 화면 정체성 강화', 'category': 'GitHub', 'priority': '높음', 'status': '진행 필요', 'output': 'PT 트레이너를 위한 회원 변화 기록·상담 리포트 SaaS MVP 설명', 'risk': '저장소 메타데이터 수정 권한 확인 필요'},
        ]
        for item in strategies:
            StrategyItem.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('LIGHT ONE demo data and login accounts created.'))
        self.stdout.write('Login accounts: admin/admin, member1/1234, member2/1234')
