# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.apps import apps
from common.services.common import get, post, patch, delete

import json
from order.models.details.OrderProduct import OrderProduct

@api_view(['POST'])
def create(request, format=None):

	response = post(request, OrderProduct)

	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)

@api_view(['POST'])
def read(request, format=None):

	response = get(request, OrderProduct)

	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)

@api_view(['POST'])
def update(request, format=None):

	response = patch(request, OrderProduct)

	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)

@api_view(['POST'])
def delete(request, format=None):

	response = delete(request, OrderProduct)
	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)
