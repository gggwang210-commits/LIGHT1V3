# LIGHT ONE 포트폴리오 제출 전 체크리스트

## 1. 문서 목적

이 문서는 LIGHT ONE 프로젝트를 GitHub, 사업계획서, 멘토링, 심사 발표, 포트폴리오에 제출하기 전에 누락된 항목과 위험 표현을 점검하기 위한 체크리스트입니다.

LIGHT ONE은 현재 완성된 상용 서비스가 아니라, PT·피트니스 현장의 상담 리포트 신뢰도를 보조하기 위한 촬영 품질 확인, 조명 품질 측정, 카메라 보정, 촬영 부스 QC 기술 증빙 MVP입니다.

## 2. GitHub 기본 상태 확인

제출 전 아래 명령어를 실행합니다.

```bash
git switch main
git pull origin main
git status
python -m pip install -r requirements.txt
