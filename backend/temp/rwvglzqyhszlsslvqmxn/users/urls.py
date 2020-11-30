# -*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [

	url(r'^sub_component_1/', include('users.routes.sub_component_1.urls')),
	url(r'^sub_component_2/', include('users.routes.sub_component_2.urls')),
	url(r'^sub_component_3/', include('users.routes.sub_component_3.urls')),
	url(r'^sub_component_4/', include('users.routes.sub_component_4.urls')),

]
	