# -*- coding: utf-8 -*-
from rest_framework import serializers
from order.models.details.Order import Order

class OrderSerializer(serializers.ModelSerializer):

	class Meta:

		model = Order
		fields = (

			'id',
			'firstName',
			'lastName',
			'emailId',
			'phoneNumber',
			'createdAt',
			'updatedAt'
		)
