from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.RedirectView.as_view(), name="index"),
                       url(r'^\home$', views.UserLandingPage.as_view(), name="home"),
                       )