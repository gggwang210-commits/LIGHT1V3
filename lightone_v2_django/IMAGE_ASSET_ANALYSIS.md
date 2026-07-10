# LIGHT ONE 이미지 파일 분석 및 반영 내역

## 결론
첨부된 `img.zip` 이미지는 LIGHT ONE 장고 프로젝트의 정적 파일 경로 `static/lightone/img/`에 모두 포함했다. 첫 대시보드에는 `dashbord.png`, `healthcare_main_gym.png`, `one.png`, `time.png`, `11_01_dotted_wave_pattern.png` 등 비의료 운동상담 이미지와 데이터 패턴을 직접 연결해 이미지가 실제 화면에 보이도록 구성했다.

## 이미지별 용도 판단

| 파일명 | 크기 | 판단 용도 | 반영 위치 |
|---|---:|---|---|
| `dashbord.png` | 1774x887 | 갤럭시탭/태블릿 기반 대시보드 핵심 이미지 | 첫 히어로 섹션 우측 프리뷰 |
| `base.png` | 1626x967 | 운동상담 배경, 프리미엄 SaaS 분위기 | 보관, 외부 배포 화면에서는 미사용 |
| `base2.png` | 1448x1086 | 스카이톤 웰니스·운동 데이터 배경 | 보관, 외부 배포 화면에서는 미사용 |
| `one.png` | 1624x969 | 관절·움직임 분석 콘셉트 | 이미지 소스 분석 카드 |
| `time.png` | 1636x961 | 웨어러블 건강 데이터 콘셉트 | 이미지 소스 분석 카드 |
| `hartbeat.png` | 1314x756 | 운동 리듬·컨디셔닝 데이터 패턴 | 보관, 외부 배포 화면에서는 패턴 이미지로 대체 |
| `runner.png` | 202x126 | 러닝/운동 아이콘성 이미지 | 정적 파일 보관 |
| `04_card_panel_background.png` | 367x187 | 카드형 UI 배경 | 정적 파일 보관 및 기존 CSS 유지 |
| `05_chart_panel_background.png` | 367x154 | 차트형 UI 배경 | 정적 파일 보관 및 기존 CSS 유지 |
| `08_content_section_background.png` | 440x164 | 콘텐츠 섹션 배경 | 정적 파일 보관 및 기존 CSS 유지 |
| `11_01~11_05` 패턴 이미지 | 약 280~309x95 | 배경 패턴/텍스처 | 기존 CSS 및 배경 효과 유지 |
| `phone_hand_light.png` | 1619x971 | 스마트폰/모바일 컨디셔닝 보조 이미지 | 원본 이상 파일명 정규화 보관 |
| `healthcare_main_gym.png` | 2172x724 | 운동상담 메인 배너형 이미지 | 원본 이상 파일명 정규화 보관 |

## 랜딩/대시보드 노출 점검

- 외부 배포용 랜딩/대시보드에서는 의료 플러스, 병원 복도, DNA 텍스처 이미지를 직접 노출하지 않는다.
- 상세 히어로 배경은 의료 명칭이 포함된 슬림 히어로 이미지 대신 소프트 웨이브 그라디언트 패턴을 사용한다.
- 메인 히어로와 이미지 소스 분석 카드는 운동상담 맥락의 배너 이미지와 비의료 데이터 패턴을 우선 사용한다.

## 코드 반영 파일

- `templates/lightone/dashboard.html`
  - `{% load static %}` 추가
  - 히어로 섹션에 태블릿 대시보드 이미지 삽입
  - `이미지 소스 분석 반영` 섹션 추가

- `static/lightone/css/lightone.css`
  - `image-hero`, `hero-visual`, `asset-grid`, `asset-card` 스타일 추가
  - 모바일에서는 태블릿 프리뷰를 숨겨 화면 깨짐 방지

## 안전 경계
이 프로젝트는 의료 진단·치료 목적이 아니라, PT 상담 및 웰니스 리포트 프로토타입이다. 이미지와 화면 문구도 의료 판정처럼 보이지 않도록 `Non-medical`, `Human-in-the-loop`, `Safety Boundary` 문구를 유지했다.
