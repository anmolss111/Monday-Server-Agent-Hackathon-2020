# -*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [

	url(r'^details/', include('order.routes.details.urls')),

]
	