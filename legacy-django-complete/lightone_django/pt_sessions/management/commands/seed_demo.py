"""
LIGHT ONE 더미 데이터 시딩 명령어
사용법: python manage.py seed_demo
"""
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import TrainerProfile
from members.models import Member
from pt_sessions.models import MemberSession

User = get_user_model()

MEMBER_DATA = [
    {"name": "김민준", "age": 32, "sex": "M", "goal": "posture", "discomfort_area": "허리, 어깨"},
    {"name": "이서연", "age": 28, "sex": "F", "goal": "pain", "discomfort_area": "무릎"},
    {"name": "박지훈", "age": 45, "sex": "M", "goal": "weight", "discomfort_area": "없음"},
    {"name": "최수아", "age": 35, "sex": "F", "goal": "posture", "discomfort_area": "골반, 척추"},
    {"name": "정태양", "age": 27, "sex": "M", "goal": "performance", "discomfort_area": "없음"},
    {"name": "한예린", "age": 41, "sex": "F", "goal": "rehab", "discomfort_area": "발목, 무릎"},
    {"name": "오준혁", "age": 38, "sex": "M", "goal": "strength", "discomfort_area": "어깨"},
    {"name": "윤지아", "age": 30, "sex": "F", "goal": "posture", "discomfort_area": "목, 어깨"},
]

EXERCISES = ["스쿼트", "데드리프트", "런지", "레그프레스", "플랭크", "힙힌지", "케이블 로우", "숄더프레스"]


class Command(BaseCommand):
    help = "LIGHT ONE 데모용 더미 데이터를 생성합니다."

    def handle(self, *args, **kwargs):
        self.stdout.write("=== LIGHT ONE 더미 데이터 시딩 시작 ===")

        # 1. 트레이너 계정 생성
        if not User.objects.filter(username="trainer01").exists():
            user = User.objects.create_user(
                username="trainer01",
                password="lightone2026",
                display_name="송광일 트레이너",
                role="trainer",
            )
            TrainerProfile.objects.create(
                user=user,
                center_name="LIGHT ONE PT 센터",
                specialty="체형교정, 통증관리",
                bio="7년 경력 퍼스널 트레이너",
            )
            self.stdout.write(self.style.SUCCESS("✓ 트레이너 계정 생성: trainer01 / lightone2026"))
        else:
            user = User.objects.get(username="trainer01")
            self.stdout.write("- 트레이너 계정 이미 존재")

        trainer_profile = user.trainer_profile

        # 2. 관리자 계정 생성
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                password="admin1234",
                display_name="관리자",
                role="admin",
            )
            self.stdout.write(self.style.SUCCESS("✓ 관리자 계정 생성: admin / admin1234"))

        # 3. 회원 생성
        members = []
        for d in MEMBER_DATA:
            m, created = Member.objects.get_or_create(
                name=d["name"],
                defaults={
                    "trainer": trainer_profile,
                    "age": d["age"],
                    "sex": d["sex"],
                    "goal": d["goal"],
                    "discomfort_area": d["discomfort_area"],
                }
            )
            members.append(m)
            if created:
                self.stdout.write(f"  ✓ 회원 등록: {m.name}")

        self.stdout.write(self.style.SUCCESS(f"✓ 총 {len(members)}명 회원 준비 완료"))

        # 4. 세션 데이터 생성 (회원당 8~12회)
        session_count = 0
        today = date.today()
        for member in members:
            if MemberSession.objects.filter(member=member).exists():
                continue
            num_sessions = random.randint(8, 12)
            for i in range(num_sessions):
                session_date = today - timedelta(days=(num_sessions - i) * 3 + random.randint(0, 2))
                pain = round(random.uniform(0, 4 if member.discomfort_area != "없음" else 1.5), 1)
                rpe = round(random.uniform(5, 9), 1)
                form_acc = round(random.uniform(5, 9.5), 1)
                jatc = round(random.uniform(55, 90), 1)
                shoulder_tilt = round(random.uniform(-3, 3), 1)
                pelvis_tilt = round(random.uniform(-2, 2), 1)
                spine_aln = round(random.uniform(5, 9.5), 1)
                knee_aln = round(random.uniform(5, 9.5), 1)
                ankle_aln = round(random.uniform(5, 9.5), 1)
                lr_dev = round(random.uniform(-2, 2), 1)

                s = MemberSession(
                    member=member,
                    trainer=trainer_profile,
                    session_date=session_date,
                    exercise_name=random.choice(EXERCISES),
                    sets=random.choice([3, 4]),
                    reps=random.choice([8, 10, 12]),
                    weight_kg=round(random.uniform(20, 80), 1),
                    pain_response=pain,
                    rpe=rpe,
                    form_accuracy=form_acc,
                    jatc_score=jatc,
                    shoulder_tilt=shoulder_tilt,
                    pelvis_tilt=pelvis_tilt,
                    spine_alignment=spine_aln,
                    knee_alignment=knee_aln,
                    ankle_alignment=ankle_aln,
                    lr_deviation=lr_dev,
                    qc_status=random.choices(["PASS", "CHECK", "FAIL"], weights=[80, 15, 5])[0],
                    memo="",
                )
                s.save()
                s.calculate_qs_and_route()
                session_count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ 총 {session_count}개 세션 데이터 생성 완료"))
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=== 시딩 완료 ==="))
        self.stdout.write("접속 정보:")
        self.stdout.write("  트레이너: trainer01 / lightone2026")
        self.stdout.write("  관리자:   admin / admin1234")
        self.stdout.write("  URL:      http://127.0.0.1:8000/")
