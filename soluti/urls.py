# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include

urlpatterns = patterns('',
    (r'^$', 'soluti.views.index'),
    (r'^admin/$', 'soluti.views.index'),
    (r'', include('djangoplus.core.urls')),
)
