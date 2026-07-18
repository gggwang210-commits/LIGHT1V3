---
pretty_name: LIGHT ONE PT Survey - De-identified Research Export
language:
- ko
license: other
task_categories:
- tabular-classification
tags:
- survey
- fitness
- non-medical
- de-identified
configs:
- config_name: deidentified
  data_files:
  - split: train
    path: data/deidentified/*.jsonl
---

# LIGHT ONE PT Survey - De-identified Research Export

이 데이터 카드는 LIGHT ONE의 AI 기반 PT 시스템 연구 설문 결과를 **비식별 집계 또는 합성 데이터**로만 다루기 위한 초안입니다.

## Publication status

현재 원본 설문에는 선택적 연락처와 자유서술이 포함될 수 있으므로 공개 업로드를 허용하지 않습니다. 비식별 검토가 끝나기 전에는 Hugging Face Dataset 저장소를 **private**으로 유지해야 합니다.

## Intended use

- 센터장·트레이너·회원 집단별 기능 필요도 탐색
- 문항별 분포와 파일럿 가설 생성
- 비의료 PT 상담 운영 시스템의 사용자 경험 연구

## Prohibited use

- 개인 식별 또는 재식별
- 의료 진단, 치료, 재활 판정
- 고용·보험·가격 차별 의사결정
- 원본 연락처 또는 자유서술 공개
- 표본 대표성이 검증되지 않은 상태에서 일반화된 시장 주장

## Features

| 필드 | 형식 | 설명 |
|---|---|---|
| `anonymous_id` | string | 원본 ID를 복원할 수 없는 무작위/해시 식별자 |
| `received_month` | `YYYY-MM` | 일시를 월 단위로 축소 |
| `role` | enum | `owner`, `coach`, `member` |
| `answers` | object | 해당 역할의 15개 문항, 1~5 정수 |
| `source_version` | string | 문항 버전 |
| `deidentified` | boolean | 항상 `true` |

## De-identification

다음 필드는 내보내기 전에 제거합니다.

- 이름 또는 담당자명
- 소속 센터·기관
- 이메일
- 전화번호
- 자유서술
- PDF URL과 파일 ID
- 원본 응답 ID와 요청 ID
- 오류 메시지 원문

날짜는 월 단위로 축소하고, 소수 집단의 재식별 가능성을 별도로 검토합니다.

## Limitations

- 편의표본 설문이므로 전체 PT 시장을 대표하지 않습니다.
- 자기보고 응답이며 실제 행동이나 지불의사를 보증하지 않습니다.
- 역할별 표본 수가 작을 때 집단 비교가 불안정할 수 있습니다.
- 비식별 처리는 재식별 위험을 완전히 제거한다고 보장할 수 없습니다.

## Governance

원본은 Google Drive/Sheet의 제한된 운영 영역에 보관합니다. 분석용 파일은 `schemas/public-export.schema.json`을 통과한 별도 산출물만 사용합니다. 외부 공개 전 개인정보·계약·보유기간 검토가 필요합니다. `[검증필요]`

