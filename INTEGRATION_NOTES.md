# LIGHT1V3 통합본

V2 Django 본체를 기준으로 V1의 품질관리(QC), 카메라 캘리브레이션, 조명 정규화 모듈을 통합한 저장소입니다.

## 구성

- `lightone_v2_django/`: V2 Django 애플리케이션
- `camera_calibration/`: 카메라 캘리브레이션 도구
- `center_qc/`: 센터 품질관리 모듈
- `lighting_normalization/`: 조명 정규화 모듈
- `quality_pipeline.py`: 품질 파이프라인 진입점
- `docs/LIGHT_ONE_V2_Django_통합_개발_계획_전략서_2026-07-10.docx`: 통합 개발 계획서
- `legacy/v1/`, `legacy/v2/`: 통합 전 원본 보존본

민감한 환경변수 파일과 생성 산출물은 커밋 대상에서 제외합니다.
