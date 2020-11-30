# -*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [

	url(r'^sub_component_1/', include('polls.routes.sub_component_1.urls')),
	url(r'^sub_component_2/', include('polls.routes.sub_component_2.urls')),

]
	