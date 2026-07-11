from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import SignupForm


class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
