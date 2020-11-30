# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

import products.views.branding.Brand as BrandView
import products.views.branding.Section as SectionView
urlpatterns = {

	url(r'^brand/create$', BrandView.create), 
	url(r'^brand/read$', BrandView.read), 
	url(r'^brand/update$', BrandView.update), 
	url(r'^brand/delete$', BrandView.delete), 
	url(r'^section/create$', SectionView.create), 
	url(r'^section/read$', SectionView.read), 
	url(r'^section/update$', SectionView.update), 
	url(r'^section/delete$', SectionView.delete), 
}

urlpatterns = format_suffix_patterns(urlpatterns)