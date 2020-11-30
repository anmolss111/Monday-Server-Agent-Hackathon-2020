# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

import products.views.products.Product as ProductView
urlpatterns = {

	url(r'^product/create$', ProductView.create), 
	url(r'^product/read$', ProductView.read), 
	url(r'^product/update$', ProductView.update), 
	url(r'^product/delete$', ProductView.delete), 
}

urlpatterns = format_suffix_patterns(urlpatterns)