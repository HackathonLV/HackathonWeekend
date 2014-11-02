from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from forms import *


class UserLandingPage(FormView):
    template_name = 'SampleLogon.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = form.cleaned_data['username']
        password = form.cleaned_data['password']

        print user, password

        return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})