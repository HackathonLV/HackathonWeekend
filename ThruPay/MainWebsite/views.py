from django.shortcuts import render
from django.views.generic import TemplateView


class UserLandingPage(TemplateView):
    template_name = 'SampleLogon.html'
    def get(self, request, *args, **kwargs):
        user = request.user
        password = request.password

        context = {}
        context['user'] = user
        context['password'] = password

        return render(request, self.template_name, context)