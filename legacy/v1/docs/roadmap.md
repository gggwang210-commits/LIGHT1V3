# LIGHT ONE 기술 로드맵

> 규칙 기반 → ML → MediaPipe 순서로 단계적 고도화

---

## Phase 1 — 규칙 기반 MVP (현재 ~ 2개월)

**목표:** 상담에 바로 쓸 수 있는 리포트 자동 생성

### 완료된 기술 모듈

| 모듈 | 위치 | 기능 |
|---|---|---|
| Camera Calibration | `camera_calibration/` | 촬영 품질 PASS/CHECK/FAIL 분류 |
| Lighting Normalization | `lighting_normalization/` | 조명 조건 자동 보정 |
| Center QC | `demo_assets/center_qc/` | 촬영 환경 품질 게이트 |

### 개발 중 (웹 레이어)

```text
상담 입력폼 (Django)
  → QS 규칙 기반 산출 엔진
  → JATC 규칙 기반 산출 엔진
  → AUTO/REVIEW/BLOCK 라우팅
  → 트레이너 검토 플로우 (Human-in-the-loop)
  → 상담 리포트 자동 생성 (PDF/웹)
  → 원장 대시보드 (트레이너별 상담 이력)
```

### 심사 가시성

- 더미 데이터 기반 데모 리포트 3종
- GitHub 실행 화면 캡처
- 트레이너 검토 플로우 시연 가능

---

## Phase 2 — ML 기반 패턴 분석 (3~6개월)

**목표:** 데이터 누적 → 패턴 학습 → 예측 보조

### 기술 스택

```text
상담 패턴 분석:
- XGBoost / LightGBM
- QS 추세 → 다음 세션 부하 제안
- JATC 변화 패턴 → 조기 이탈 예측
- 통증 반응 패턴 → 위험 신호 조기 탐지

자세 포인트 자동 인식:
- MediaPipe (Google) / OpenPose v1.7.0
- 마커 없이 관절 포인트 추출
- 관절 가동범위(ROM) 자동 산출
- 비대칭 지수 자동 계산
- 표준 촬영 조건: 거리 2.5m, 조명 500lux↑ [확인필요]
```

### 근거 논문

- Cao Z et al. (2017). OpenPose. *CVPR*. doi:10.1109/CVPR.2017.143
- Mathis A et al. (2018). DeepLabCut. *Nat Neurosci*, 21(9).

### 데이터 요구사항

- 최소 세션 수: 파일럿 센터 3곳 × 30명 × 16세션 = 1,440 세션 [확인필요]
- JATC 가중치 최적화: 전문가 델파이 조사 (3회, 전문가 8명) [확인필요]
- QS 신뢰도 검증: ICC (급내상관계수) ≥ 0.75 [확인필요]

---

## Phase 3 — 개인화 AI 추천 (6~12개월)

**목표:** 회원별 맞춤 운동 처방 보조

```text
회원 프로필 + 세션 이력 + QS·JATC 추세
  → 다음 세션 운동 구성 자동 제안
  → 통증 위험 신호 사전 탐지
  → 재등록 가능성 예측 (원장 대시보드)

보안 강화:
  → Federated Learning (연합학습) 도입 검토
  → 센터 간 데이터 공유 없이 모델 고도화
```

---

## KPI (단계별 측정 지표)

| 단계 | KPI | 목표값 |
|---|---|---|
| Phase 1 | 리포트 생성 성공률 | ≥ 95% |
| Phase 1 | 트레이너 검토 완료율 | ≥ 90% |
| Phase 2 | QS 신뢰도 (ICC) | ≥ 0.75 [확인필요] |
| Phase 2 | JATC 예측 정확도 | 탐색적 모델링 후 확정 |
| Phase 3 | 파일럿 센터 재계약률 | ≥ 80% [확인필요] |
| Phase 3 | 원장 대시보드 월 활성 사용률 | ≥ 70% [확인필요] |

---

## 개발 스프린트 계획

```text
Week 1~2  : Django 상담 입력폼 완성
Week 3~4  : 규칙 기반 QS 산출 엔진 구현
Week 5~6  : JATC 산출 + AUTO/REVIEW/BLOCK 라우팅
Week 7~8  : 트레이너 검토 플로우 (HITL)
Week 9~10 : 상담 리포트 자동 생성 (PDF)
Week 11~12: 원장 대시보드 + 파일럿 준비
```

---

## 참고문헌 (기술 로드맵 근거)

```text
[영상 분석]
Cao Z et al. (2017). Realtime multi-person 2D pose estimation. CVPR.
Mathis A et al. (2018). DeepLabCut. Nature Neuroscience, 21(9).

[ML / 디지털 헬스]
LeCun Y, Bengio Y, Hinton G. (2015). Deep learning. Nature, 521(7553).
Topol EJ. (2019). High-performance medicine. Nature Medicine, 25(1).
Rieke N et al. (2020). Federated learning in digital health. NPJ Digital Medicine, 3.

[운동 처방 / 통증]
ACSM. (2025). Guidelines for Exercise Testing and Prescription. 12th ed. [확인필요]
Schoenfeld BJ. (2010). Muscle hypertrophy mechanisms. J Strength Cond Res.
Farrar JT et al. (2001). NRS pain scale. Pain, 94(2).
```

---

*LIGHT ONE — 프로의 기준, 이제는 데이터입니다.*
