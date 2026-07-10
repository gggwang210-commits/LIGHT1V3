from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve

def _resolve_url_name(path):
    try:
        match = resolve(path)
    except Exception:
        return None
    return f'{match.namespace}:{match.url_name}' if match.namespace else match.url_name

class LoginRequiredMiddleware:
    """
    프로젝트 전역 접근 제어 미들웨어. (COPD 프로젝트 구조 차용)
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        if path.startswith(settings.STATIC_URL) or path.startswith('/admin/'):
            return self.get_response(request)

        url_name = _resolve_url_name(path)

        if request.user.is_authenticated:
            guest_only_names = getattr(settings, 'GUEST_ONLY_URL_NAMES', [])
            if url_name in guest_only_names:
                return redirect('lightone:dashboard')
            return self.get_response(request)

        exempt_names = getattr(settings, 'LOGIN_EXEMPT_URL_NAMES', [])
        if url_name in exempt_names:
            return self.get_response(request)

        login_url = getattr(settings, 'LOGIN_URL', 'accounts:login')
        return redirect(login_url)
