from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/admin/', permanent=True), name='home'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
