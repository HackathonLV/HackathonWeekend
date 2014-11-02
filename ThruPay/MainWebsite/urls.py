from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.UserLandingPage.as_view(), name="home"),
                       )