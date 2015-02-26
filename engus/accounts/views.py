from django.views.generic.base import TemplateView
from braces.views import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context
