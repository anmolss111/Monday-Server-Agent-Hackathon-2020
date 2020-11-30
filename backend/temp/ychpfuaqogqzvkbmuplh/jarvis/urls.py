# -*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [

	url(r'^products/', include('products.urls')),
	url(r'^order/', include('order.urls')),

]
