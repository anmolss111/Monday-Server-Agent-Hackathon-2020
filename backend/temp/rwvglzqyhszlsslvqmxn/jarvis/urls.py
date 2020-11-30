# -*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [

	url(r'^users/', include('users.urls')),
	url(r'^polls/', include('polls.urls')),

]
