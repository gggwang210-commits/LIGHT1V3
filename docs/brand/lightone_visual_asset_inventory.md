# LIGHTONE V2 Visual Asset Inventory

## 결론

이 문서는 사용자가 제작한 LIGHTONE 시각 자료를 Django MVP, 랜딩페이지, 발표자료, 포트폴리오에 재사용하기 위한 자산 목록입니다.

현재 자산은 의료 진단·치료·처방용 UI가 아니라 **비의료 PT 상담 보조 SaaS / 컨디셔닝 운영 지원 시스템**의 브랜드·제품 표현 자료로 사용합니다.

## 적용 위치

```text
lightone_v2_django/static/lightone/img/brand/
lightone_v2_django/static/lightone/css/brand_visual_assets.css
```

## 자산 목록

| Slug | Category | Repo Path | Recommended Use |
|---|---|---|---|
| `studio-interior-night-blue` | hero/background | `lightone_v2_django/static/lightone/img/brand/studio-interior-night-blue.webp` | Django landing page dark hero/background |
| `dashboard-icon-set` | icon/source | `lightone_v2_django/static/lightone/img/brand/dashboard-icon-set.webp` | Reference source for sidebar/dashboard icon style; not final UI icon sprite |
| `studio-interior-day` | landing/hero | `lightone_v2_django/static/lightone/img/brand/studio-interior-day.webp` | Landing page premium day hero |
| `studio-interior-night-warm` | landing/hero | `lightone_v2_django/static/lightone/img/brand/studio-interior-night-warm.webp` | Landing page premium night hero |
| `studio-interior-night-blue-alt` | background | `lightone_v2_django/static/lightone/img/brand/studio-interior-night-blue-alt.webp` | Dark premium SaaS hero or section background |
| `trainer-feedback-dashboard` | dashboard/mockup | `lightone_v2_django/static/lightone/img/brand/trainer-feedback-dashboard.webp` | Portfolio/mockup preview of member feedback report UI |
| `ai-fitness-overlay-bg` | background | `lightone_v2_django/static/lightone/img/brand/ai-fitness-overlay-bg.webp` | AI analytics visual section background |
| `network-abstract-bg` | background | `lightone_v2_django/static/lightone/img/brand/network-abstract-bg.webp` | Data architecture/RAG/AI section background |
| `studio-exterior-day` | landing/exterior | `lightone_v2_django/static/lightone/img/brand/studio-exterior-day.webp` | Brand story or studio concept exterior visual |

## 사용 원칙

- 실제 회원 얼굴, 연락처, 건강정보, 상담기록과 결합하지 않습니다.
- “진단”, “치료”, “처방”, “질병 위험도 예측”, “환자 모니터링” 표현과 함께 사용하지 않습니다.
- 화면 하단 또는 설명문에 “비의료 운동상담 참고용 / 트레이너 검토 필요” 문구를 유지합니다.
- GitHub 공개 저장소에서는 합성 이미지·비식별 샘플 데이터임을 명확히 표시합니다.

## Django 템플릿 예시

```django
{% load static %}
<link rel="stylesheet" href="{% static 'lightone/css/brand_visual_assets.css' %}">

<section class="lo-hero-visual lo-hero-night">
  <div class="container">
    <p class="lo-nonmedical-caption">
      비의료 PT 상담 참고용 · 트레이너 검토 필요
    </p>
  </div>
</section>
```

## 다음 작업

1. 랜딩페이지 hero 영역에 `studio-interior-day.webp` 또는 `studio-interior-night-warm.webp` 적용
2. 대시보드 소개 섹션에 `trainer-feedback-dashboard.webp` 적용
3. AI 분석 설명 섹션에 `ai-fitness-overlay-bg.webp` 적용
4. README에 대표 스크린샷 1~2개 추가
