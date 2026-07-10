// LIGHT ONE — 프론트엔드 유틸리티

// 날짜 표시
const dateEl = document.getElementById('topbarDate');
if (dateEl) {
  const now = new Date();
  const opts = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'short' };
  dateEl.textContent = now.toLocaleDateString('ko-KR', opts);
}

// 사이드바 토글 (모바일)
const toggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
if (toggle && sidebar) {
  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });
}

// QS 점수 바 색상 동적 적용
document.querySelectorAll('.lo-qs-fill').forEach(el => {
  const val = parseFloat(el.style.width) || 0;
  if (val < 40) el.classList.add('low');
  else if (val < 70) el.classList.add('mid');
});

// 알림 자동 닫기 (3초)
setTimeout(() => {
  document.querySelectorAll('.lo-alert').forEach(el => {
    const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
    if (bsAlert) bsAlert.close();
  });
}, 3500);
