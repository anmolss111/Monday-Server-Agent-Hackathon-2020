# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

import users.views.sub_component_1.Users as UsersView
import users.views.sub_component_1.Table3 as Table3View
urlpatterns = {

	url(r'^users/create$', UsersView.create), 
	url(r'^users/read$', UsersView.read), 
	url(r'^users/update$', UsersView.update), 
	url(r'^users/delete$', UsersView.delete), 
	url(r'^table3/create$', Table3View.create), 
	url(r'^table3/read$', Table3View.read), 
	url(r'^table3/update$', Table3View.update), 
	url(r'^table3/delete$', Table3View.delete), 
}

urlpatterns = format_suffix_patterns(urlpatterns)