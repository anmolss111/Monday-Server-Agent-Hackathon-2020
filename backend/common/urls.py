from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

import common.views.common as CommonView

urlpatterns = {

	url(r'^service$', CommonView.service),

}

urlpatterns = format_suffix_patterns(urlpatterns)
