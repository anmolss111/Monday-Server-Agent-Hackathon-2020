# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

import users.views.sub_component_2.Table4 as Table4View
urlpatterns = {

	url(r'^table4/create$', Table4View.create), 
	url(r'^table4/read$', Table4View.read), 
	url(r'^table4/update$', Table4View.update), 
	url(r'^table4/delete$', Table4View.delete), 
}

urlpatterns = format_suffix_patterns(urlpatterns)