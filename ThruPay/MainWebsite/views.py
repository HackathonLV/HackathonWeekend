from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from forms import *
import random
import time
import paypalrestsdk
from auth import *


endpoints={
    'AUTHORIZATION_ENDPOINT': 'https://www.paypal.com/webapps/auth/protocol/openidconnect/v1/authorize',
    'ACCESS_TOKEN_ENDPOINT': 'https://api.paypal.com/webapps/auth/protocol/openidconnect/v1/tokenservice',
    'PROFILE_ENDPOINT': 'https://www.paypal.com/webapps/auth/protocol/openidconnect/v1/userinfo',
    'LOGOUT_ENDPOINT': 'https://www.paypal.com/webapps/auth/protocol/openidconnect/v1/endsession',
    'VALIDATE_ENDPOINT': 'https://www.paypal.com/webapps/auth/protocol/openidconnect/v1/checkid',
    'SANDBOX_ENDPOINT' : 'https://sandbox.paypal.com/webapps/auth/protocol/openidconnect/v1/authorize'
}


def buildRedirectUrl():
    nonce = time.time() * random.randint(0, 100)
    state = time.time() * random.randint(0, 100)
    auth_url = "%s?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&nonce=%s&state=%s" % (
                            endpoints['SANDBOX_ENDPOINT'],
                            'ThruPay',
                            'openid',
                            'http://127.0.0.1:8000', # Fill this in with a real url
                            nonce,
                            state)

    return auth_url

class RedirectView( TemplateView ):
    template_name = ''
    ppaccess = PayPalAccess()
    params = cgi.FieldStorage()

    def get(self, request, *args, **kwargs):
        if self.params.has_key('code'):
            print 'Content-Type: text/plain'
            print ''

            #get access token
            token = self.ppaccess.get_access_token(self.params['code'].value)
            print token

            #get user profile
            profile = self.ppaccess.get_profile()
            print "<h1>Profile</h1>"
            print profile

            #refresh access token
            refreshed = self.ppaccess.refresh_access_token()
            print "<h1>Refreshed Token</h1>"
            print refreshed

            #validate the id token and provide back validation object
            verify = self.ppaccess.validate_token()
            print "<h1>Validated Token</h1>"
            print verify

            #log the user out
            # self.ppaccess.end_session()
        else:
            #get auth url and redirect user browser to PayPal to log in
            url = buildRedirectUrl()
            return redirect(url)

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