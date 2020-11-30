# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.apps import apps
from common.services.common import get, post, patch, delete

import json
from users.models.sub_component_1.Users import Users

@api_view(['POST'])
def create(request, format=None):

	response = post(request, Users)

	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)

@api_view(['POST'])
def read(request, format=None):

	response = get(request, Users)

	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)

@api_view(['POST'])
def update(request, format=None):

	response = patch(request, Users)

	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)

@api_view(['POST'])
def delete(request, format=None):

	response = delete(request, Users)
	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)
