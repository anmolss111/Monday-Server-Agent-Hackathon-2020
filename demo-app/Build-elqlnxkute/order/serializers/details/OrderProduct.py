# -*- coding: utf-8 -*-
from rest_framework import serializers
from order.models.details.OrderProduct import OrderProduct

class OrderProductSerializer(serializers.ModelSerializer):

	class Meta:

		model = OrderProduct
		fields = (

			'id',
			'order_id',
			'product_id',
			'createdAt',
			'updatedAt'
		)
