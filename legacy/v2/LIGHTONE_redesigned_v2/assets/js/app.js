const routes = [
  { slug: 'home', nav: 'Home', title: 'AI 기반 신체 변화 분석을 더 단순하고 선명하게', eyebrow: 'LIGHTONE V2', lead: 'LIGHTONE은 촬영 기반 신체 데이터를 AI로 해석해 사용자와 트레이너가 변화의 원인과 다음 행동을 빠르게 이해하도록 돕는 헬스케어 분석 플랫폼입니다.', points: ['정적 검토용 단일 페이지', '해시 라우터 기반 섹션 전환', '제안서·IR·파일럿 설명에 최적화'], metric: '11 Routes', cta: '문제 정의 보기', next: 'problem' },
  { slug: 'problem', nav: 'Problem', title: '운동 성과는 기록되지만 변화의 이유는 설명되지 않습니다', eyebrow: 'Problem', lead: '사진, 체중, 운동 기록은 흩어져 있고 현장에서는 데이터를 해석하는 시간이 부족합니다. 사용자는 무엇을 바꿔야 하는지, 트레이너는 어떤 지점을 코칭해야 하는지 즉시 알기 어렵습니다.', points: ['분산된 촬영·상담·운동 기록', '주관적 피드백에 의존하는 체형 평가', '반복 상담에 소모되는 운영 시간'], metric: 'Low Clarity', cta: '해결 방식 보기', next: 'solution' },
  { slug: 'solution', nav: 'Solution', title: '촬영 한 번으로 변화 신호를 구조화합니다', eyebrow: 'Solution', lead: 'LIGHTONE은 표준화된 촬영 흐름, AI 분석, 리포트 요약을 하나의 경험으로 묶어 사용자의 다음 행동을 제안합니다.', points: ['촬영 조건 가이드와 품질 체크', '변화 지표 자동 추출 및 비교', '트레이너용 상담 리포트 생성'], metric: '1 Flow', cta: 'AI 분석 보기', next: 'ai-analysis' },
  { slug: 'ai-analysis', nav: 'AI Analysis', title: 'AI 분석은 점수보다 설명 가능한 코칭에 집중합니다', eyebrow: 'AI Analysis', lead: '단순 점수화가 아니라 변화 부위, 촬영 신뢰도, 생활·운동 맥락을 함께 제시해 코칭 가능한 인사이트로 전환합니다.', points: ['포즈·실루엣 기반 변화 감지', '촬영 품질과 비교 가능성 표시', '개인별 개선 액션 제안'], metric: 'Explainable', cta: '시장 기회 보기', next: 'market' },
  { slug: 'market', nav: 'Market', title: '피트니스 현장의 디지털 전환 수요를 겨냥합니다', eyebrow: 'Market', lead: '헬스장, PT샵, 웰니스 센터는 회원 유지와 상담 효율을 위해 더 명확한 변화 증거와 자동화된 리포팅을 필요로 합니다.', points: ['회원 유지율 개선 니즈', '트레이너 생산성 향상', 'B2B SaaS 확장 가능성'], metric: 'B2B2C', cta: 'BM 보기', next: 'business-model' },
  { slug: 'business-model', nav: 'Business Model', title: '구독형 분석 리포트와 현장 운영 도구로 수익화합니다', eyebrow: 'Business Model', lead: '매장 단위 구독, 회원 분석 크레딧, 프리미엄 리포트, 파일럿 패키지를 조합해 초기 매출과 확장성을 동시에 설계합니다.', points: ['센터별 월 구독 플랜', '회원 수 기반 분석 크레딧', '데이터 리포트·컨설팅 패키지'], metric: 'SaaS', cta: '파일럿 보기', next: 'pilot-study' },
  { slug: 'pilot-study', nav: 'Pilot Study', title: '파일럿은 촬영 품질과 상담 효율을 검증합니다', eyebrow: 'Pilot Study', lead: '초기 파일럿은 실제 센터 환경에서 촬영 재현성, 리포트 이해도, 상담 시간 단축 효과를 측정합니다.', points: ['전·후면·측면 촬영 프로토콜', '트레이너 피드백 수집', '회원 행동 변화 추적'], metric: '4 Weeks', cta: '로드맵 보기', next: 'roadmap' },
  { slug: 'roadmap', nav: 'Roadmap', title: '정적 소개에서 분석 SaaS까지 단계적으로 확장합니다', eyebrow: 'Roadmap', lead: '검토용 랜딩, 파일럿 운영, 데이터 파이프라인, 관리자 대시보드, 파트너 확장 순서로 리스크를 낮춥니다.', points: ['V2 정적 소개 페이지', 'MVP 리포트 자동화', '센터용 관리자 기능', '파트너 API 연동'], metric: 'Phased', cta: '공모 제출 보기', next: 'public-submission' },
  { slug: 'public-submission', nav: 'Submission', title: '공모·지원사업 제출에 맞춘 메시지를 제공합니다', eyebrow: 'Public Submission', lead: '문제, 차별성, 실현 가능성, 시장성, 사회적 효과를 빠르게 검토할 수 있도록 페이지형 섹션으로 정리했습니다.', points: ['심사 관점별 핵심 문장', '기술성과 사업성의 균형', '파일럿 기반 검증 계획'], metric: 'Review Ready', cta: '홍보 전략 보기', next: 'promotion' },
  { slug: 'promotion', nav: 'Promotion', title: '변화를 보여주는 콘텐츠가 가장 강력한 홍보 자산입니다', eyebrow: 'Promotion', lead: '비포·애프터 비교, AI 리포트 스냅샷, 트레이너 코칭 사례를 중심으로 신뢰 가능한 콘텐츠 루프를 만듭니다.', points: ['센터 도입 사례 카드', '회원 변화 스토리', 'SNS용 리포트 이미지'], metric: 'Proof Loop', cta: '문의하기', next: 'contact' },
  { slug: 'contact', nav: 'Contact', title: '파일럿과 파트너십 논의를 시작하세요', eyebrow: 'Contact', lead: 'LIGHTONE redesigned v2는 정적 배포 가능한 검토본입니다. 도입 검토, 공모 제출, 데모 제작을 위한 다음 단계를 연결합니다.', points: ['파일럿 센터 모집', '공모 제출 자료 정리', 'MVP 기능 우선순위 협의'], metric: 'Next Step', cta: '처음으로', next: 'home' }
];

const routeMap = new Map(routes.map((route) => [route.slug, route]));
const app = document.querySelector('#app');
const nav = document.querySelector('#route-nav');
const toggle = document.querySelector('.nav-toggle');

function buildNav() {
  nav.innerHTML = routes.map((route) => `<a href="#${route.slug}" data-route="${route.slug}">${route.nav}</a>`).join('');
}

function getRoute() {
  const slug = window.location.hash.replace('#', '') || 'home';
  return routeMap.get(slug) || routeMap.get('home');
}

function render() {
  const route = getRoute();
  document.title = `${route.title} | LIGHTONE Redesigned v2`;
  app.innerHTML = `
    <article class="page" aria-labelledby="page-title">
      <section class="hero-card">
        <div class="eyebrow">${route.eyebrow}</div>
        <h1 id="page-title">${route.title}</h1>
        <p class="lead">${route.lead}</p>
        <div class="hero-actions">
          <a class="button primary" href="#${route.next}">${route.cta} →</a>
          <a class="button secondary" href="#contact">도입 문의</a>
        </div>
      </section>
      <section class="grid" aria-label="${route.nav} 핵심 내용">
        <div class="content-card">
          <h2>핵심 지표</h2>
          <div class="metric">${route.metric}</div>
          <p>현재 섹션의 검토 포인트를 한눈에 파악할 수 있도록 대표 키워드를 제공합니다.</p>
        </div>
        <div class="content-card">
          <h2>주요 내용</h2>
          <ul>${route.points.map((point) => `<li>${point}</li>`).join('')}</ul>
        </div>
        <div class="content-card">
          <h2>검토 질문</h2>
          <p>이 섹션의 메시지가 투자자, 심사위원, 파일럿 파트너에게 즉시 전달되는지 확인합니다.</p>
        </div>
      </section>
      <section class="cta-card">
        <div>
          <h2>다음 단계로 이동</h2>
          <p>모든 route는 공통 header, page title, CTA, footer 흐름을 공유합니다.</p>
        </div>
        <a class="button primary" href="#${route.next}">${route.cta}</a>
      </section>
    </article>
  `;
  nav.querySelectorAll('a').forEach((link) => {
    const isCurrent = link.dataset.route === route.slug;
    link.toggleAttribute('aria-current', isCurrent);
  });
  app.focus({ preventScroll: true });
}

buildNav();
window.addEventListener('hashchange', render);
toggle.addEventListener('click', () => {
  const expanded = toggle.getAttribute('aria-expanded') === 'true';
  toggle.setAttribute('aria-expanded', String(!expanded));
  nav.classList.toggle('open', !expanded);
});
nav.addEventListener('click', () => {
  toggle.setAttribute('aria-expanded', 'false');
  nav.classList.remove('open');
});
render();
