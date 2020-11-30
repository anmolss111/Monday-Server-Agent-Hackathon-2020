# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

import order.views.details.Order as OrderView
import order.views.details.OrderProduct as OrderProductView
urlpatterns = {

	url(r'^order/create$', OrderView.create), 
	url(r'^order/read$', OrderView.read), 
	url(r'^order/update$', OrderView.update), 
	url(r'^order/delete$', OrderView.delete), 
	url(r'^orderproduct/create$', OrderProductView.create), 
	url(r'^orderproduct/read$', OrderProductView.read), 
	url(r'^orderproduct/update$', OrderProductView.update), 
	url(r'^orderproduct/delete$', OrderProductView.delete), 
}

urlpatterns = format_suffix_patterns(urlpatterns)