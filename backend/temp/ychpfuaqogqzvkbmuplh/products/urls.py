# -*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [

	url(r'^products/', include('products.routes.products.urls')),
	url(r'^branding/', include('products.routes.branding.urls')),

]
	