# LIGHTONE Visual Source Usage Guide

## 1. 목적

이 패키지는 사용자가 제작한 LIGHTONE 시각 자료를 현재 Django MVP 프로젝트에 바로 복사해 사용할 수 있도록 정리한 것입니다.

## 2. 설치 방법

프로젝트 루트에서 압축을 풀면 다음 경로에 파일이 들어갑니다.

```bash
unzip lightone_visual_sources_ready.zip -d /workspaces/LightOne_V2
```

## 3. 포함 내용

```text
docs/brand/lightone_visual_asset_inventory.md
lightone_v2_django/static/lightone/img/brand/*.webp
lightone_v2_django/static/lightone/img/brand/asset_manifest.json
lightone_v2_django/static/lightone/css/brand_visual_assets.css
```

## 4. 권장 적용 순서

1. 먼저 Django 서버 정상 실행 확인
2. static 파일 경로 확인
3. 랜딩페이지 또는 대시보드 템플릿에 CSS 연결
4. hero 이미지 1개만 먼저 적용
5. 화면 확인 후 나머지 이미지 확장

## 5. 비의료 안전 문구

권장 문구:

> 본 화면은 비의료 PT 상담 참고용입니다. AI 및 점수 결과는 최종 판단이 아니며 트레이너 검토가 필요합니다.

## 6. 주의

이 자산은 브랜드·제품 표현용입니다. 의료 진단, 치료, 처방, 질병 예측, 환자 모니터링 화면처럼 보이게 사용하지 않습니다.
