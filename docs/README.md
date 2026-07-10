# LIGHTONE V2 Docs

이 디렉터리는 LIGHTONE V2의 사업, 제품, 운영, 검증 문서를 보관하는 문서 허브입니다.

## Canonical documents

최신 사업/제품 포지셔닝은 루트 `docs/`의 canonical documents를 기준으로 합니다. 다른 경로의 오래된 문서는 과거 검토, 구현 히스토리, 아이디어 흐름을 이해하기 위한 참고 자료이며, 현재 포지셔닝과 내용이 다를 수 있습니다.

| 문서 | 역할 |
|------|------|
| [`docs/LIGHT_ONE_final_business_plan_v1_2026-07-07.md`](LIGHT_ONE_final_business_plan_v1_2026-07-07.md) | 최종 사업계획서 기준본 |
| [`docs/product_positioning.md`](product_positioning.md) | 제품 포지셔닝 기준 문서 |
| [`docs/mvp_scope.md`](mvp_scope.md) | MVP 범위와 제외 범위 기준 문서 |
| [`docs/safety_and_privacy_policy.md`](safety_and_privacy_policy.md) | 안전·개인정보 정책 기준 문서 |
| [`docs/technical_roadmap.md`](technical_roadmap.md) | 기술 개발 로드맵 기준 문서 |
| [`docs/customer_validation_plan.md`](customer_validation_plan.md) | 고객 검증 계획 기준 문서 |
| [`docs/pitch_summary.md`](pitch_summary.md) | 발표·피치 요약 기준 문서 |

> 일부 canonical 문서는 작성 예정이거나 별도 브랜치에서 준비 중일 수 있습니다. 문서가 아직 없으면 새로 작성할 때 위 경로와 파일명을 유지합니다.

## Reference / legacy materials

아래 자료는 삭제하지 않고 보존합니다. 다만 작성 시점이 오래되었거나 전략 전환 이전의 가정이 포함될 수 있으므로, 현재 사업/제품 판단에는 위 canonical documents를 우선 적용합니다.

| 경로 | 상태 |
|------|------|
| [`lightone_v2_django/docs/`](../lightone_v2_django/docs/) | Django MVP 구현·운영 과정에서 작성된 참고 문서 |
| [`2/repo_lightoneV2/`](../2/repo_lightoneV2/) | V2 관련 자산 정리본 또는 이전 작업물 보관 영역 |
| [`아이디어-구상/`](../아이디어-구상/) | 초기 아이디어, 문제 정의, 사업 방향성 메모 보관 영역 |

## 문서 운영 원칙

- canonical documents와 reference / legacy materials의 내용이 충돌하면 canonical documents를 우선합니다.
- 오래된 문서는 현재 포지셔닝과 다를 수 있음을 명시하고, 히스토리 추적을 위해 삭제하지 않습니다.
- 문서 위치나 우선순위가 바뀌면 [`docs/repository-map.md`](repository-map.md)를 함께 업데이트합니다.
